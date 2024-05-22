import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from urllib import parse

import requests
from requests_ntlm import HttpNtlmAuth

# https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest


class SharePointSession(requests.Session):
    """A SharePoint Requests session.
    Provide session authentication to SharePoint Online sites
    in addition to standard functionality provided by Requests.
    Basic Usage::
      >>> from sharepoint import SharePointSession
      >>> sp = SharePointSessiont("example.sharepoint.com", "username", "password")
      >>> sp.get_lists()
      <Response [200]>
    """

    def __init__(self, site=None, username=None, password=None):
        super().__init__()

        self.site = re.sub(r"^https?://", "", site)
        self.expire = datetime.now(timezone.utc)  # noqa: UP017

        self.username = username
        self.password = password

        self.auth = HttpNtlmAuth(self.username, self.password)
        # Add required headers for communicating with SharePoint
        self.headers.update(
            {
                "accept": "application/json;odata=verbose",
                "content-type": "application/json;odata=verbose",
            }
        )

        self._redigest()

    def _redigest(self):
        """Check and refresh site's request form digest"""

        if self.expire <= datetime.now(timezone.utc):  # noqa: UP017
            # Avoid recursion error by not using the self.post as we call `_redigest()` in `post()`
            auth = HttpNtlmAuth(self.username, self.password)
            headers = {
                "accept": "application/json;odata=verbose",
                "content-type": "application/json;odata=verbose",
            }
            url = f"https://{self.site}/_api/contextinfo"
            r = requests.post(url, headers=headers, auth=auth, timeout=5)
            response = r.json()

            # Parse digest text and timeout
            ctx = response["d"]["GetContextWebInformation"]
            self.digest = ctx["FormDigestValue"]
            timeout = ctx["FormDigestTimeoutSeconds"]

            # Calculate digest expiry time
            self.expire = datetime.now(timezone.utc) + timedelta(seconds=timeout)  # noqa: UP017

            # Update the session headers with the digest
            self.headers.update({"x-requestdigest": self.digest})

        return self.digest

    def post(self, url, *args, **kwargs):
        """Make POST request and include x-requestdigest header"""
        if "headers" in kwargs:
            kwargs["headers"].update(**kwargs["headers"])
        # self.headers.update({"Authorization": "Bearer " + self._redigest()})
        self.headers.update({"x-requestdigest": self._redigest()})
        return super().post(url, *args, **kwargs)

    # def get(self, url, *args, **kwargs):
    #     """Make GET request and include x-requestdigest header"""
    #     # print(f"=> GET: {url}")
    #     if "headers" in kwargs.keys():
    #         kwargs["headers"].update(**kwargs["headers"])
    #     # self.headers.update({"Authorization": "Bearer " + self._redigest()})
    #     self.headers.update({"x-requestdigest": self._redigest()})
    #     return super().get(url, *args, **kwargs)

    # --------------------------------------------------------------------------
    # Helper methods
    # --------------------------------------------------------------------------

    # def get_file(self, url, *args, **kwargs):
    #     """Stream download of specified URL and output to file"""
    #     # Extract file name from request URL if not provided as keyword argument
    #     filename = kwargs.pop("filename", re.search(r"[^/]+$", url).group(0))
    #     kwargs["stream"] = True
    #     # Request file in stream mode
    #     r = self.get(url, *args, **kwargs)
    #     # Save to output file
    #     if r.status_code == requests.codes.ok:
    #         with open(filename, "wb") as file:
    #             for chunk in r:
    #                 file.write(chunk)
    #     return r

    def get_lists(self, weblist_url, **kwargs):
        """Get lists."""
        return self.get(weblist_url, **kwargs)

    def get_list_metadata_by_guid(self, weblist_url, list_guid, **kwargs):
        """Get list metadata by GUID."""
        url = f"{weblist_url}(guid'{list_guid}')"
        return self.get(url, **kwargs)

    def get_list_metadata_by_title(self, weblist_url, list_title, **kwargs):
        """Get list metadata by title."""
        list_title = parse.quote(list_title)
        url = f"{weblist_url}/getbytitle('{list_title}')"
        return self.get(url, **kwargs)

    def get_list_entity_type_by_guid(self, weblist_url, list_guid, **kwargs):
        """Get list entity type by GUID."""
        url = f"{weblist_url}(guid'{list_guid}')?$select=ListItemEntityTypeFullName"
        return self.get(url, **kwargs)

    def get_list_entity_type_by_title(self, weblist_url, list_title, **kwargs):
        """Get list entity type by title."""
        list_title = parse.quote(list_title)
        url = f"{weblist_url}/getbytitle('{list_title}')?$select=ListItemEntityTypeFullName"
        return self.get(url, **kwargs)

    def get_list_items_by_guid(self, weblist_url, list_guid, **kwargs):
        """Retrieve all list items by GUID."""
        url = f"{weblist_url}(guid'{list_guid}')/items"
        return self.get(url, **kwargs)

    def get_list_items_by_title(self, weblist_url, list_title, **kwargs):
        """Retrieve all list items by title."""
        list_title = parse.quote(list_title)
        url = f"{weblist_url}/getbytitle('{list_title}')/items"
        return self.get(url, **kwargs)

    def get_list_item_by_guid(self, weblist_url, item_id, list_guid, **kwargs):
        """Retrieve specific list item by GUID."""
        url = f"{weblist_url}(guid'{list_guid}')/items({item_id})"
        return self.get(url, **kwargs)

    def get_list_item_by_title(self, weblist_url, item_id, list_title, **kwargs):
        """Retrieve specific list item by title."""
        list_title = parse.quote(list_title)
        url = f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
        return self.get(url, **kwargs)

    def add_list_item_by_guid(self, weblist_url, payload, list_guid, headers=None):
        """Add list item by GUID."""
        url = f"{weblist_url}(guid'{list_guid}')/items"
        headers = headers or {}
        return self.post(url, json=payload, headers=headers)

    def add_list_item_by_title(self, weblist_url, payload, list_title, headers=None):
        """Add list item by title."""
        list_title = parse.quote(list_title)
        url = f"{weblist_url}/getbytitle('{list_title}')/items"
        headers = headers or {}
        return self.post(url, json=payload, headers=headers)

    def update_list_item_by_guid(  # noqa: PLR0913
        self, weblist_url, item_id, data, list_guid, headers=None
    ):
        """Update a specific list item by GUID."""
        url = f"{weblist_url}(guid'{list_guid}')/items({item_id})"
        headers = headers or {}
        headers.update({"x-http-method": "MERGE", "if-match": "*"})
        return self.post(url, json=data, headers=headers)

    def update_list_item_by_title(  # noqa: PLR0913
        self, weblist_url, item_id, data, list_title, headers=None
    ):
        """Update a specific list item by title."""
        list_title = parse.quote(list_title)
        url = f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
        headers = headers or {}
        headers.update({"x-http-method": "MERGE", "if-match": "*"})
        return self.post(url, json=data, headers=headers)

    def upload_by_guid(  # noqa: PLR0913
        self, weblist_url, item_id, content, filename, list_guid, headers=None
    ):
        """Upload a file to a list item by GUID."""
        url = (
            f"{weblist_url}(guid'{list_guid}')/items({item_id})"
            f"/AttachmentFiles/add(FileName='{filename}')"
        )

        headers = headers or {}
        headers.update({"content-length": str(len(content))})
        headers.update(**headers)
        return self.post(url, data=content, headers=headers)

    def upload_by_title(  # noqa: PLR0913
        self, weblist_url, item_id, content, filename, list_title, headers=None
    ):
        """Upload a file to a list item by title."""
        list_title = parse.quote(list_title)
        url = (
            f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
            f"/AttachmentFiles/add(FileName='{filename}')"
        )

        headers = headers or {}
        headers.update({"content-length": str(len(content))})
        headers.update(**headers)
        return self.post(url, data=content, headers=headers)

    def delete_list_item_by_guid(self, weblist_url, item_id, list_guid, headers=None):
        """Delete a specific list item by GUID."""
        url = f"{weblist_url}(guid'{list_guid}')/items({item_id})"
        headers = headers or {}
        headers.update({"x-http-method": "DELETE", "if-match": "*"})
        return self.post(url, headers=headers)

    def delete_list_item_by_title(self, weblist_url, item_id, list_title, headers=None):
        """Delete a specific list item by title."""
        list_title = parse.quote(list_title)
        url = f"{weblist_url}/getbytitle('{list_title}')/items({item_id})"
        headers = headers or {}
        headers.update({"x-http-method": "DELETE", "if-match": "*"})
        return self.post(url, headers=headers)
