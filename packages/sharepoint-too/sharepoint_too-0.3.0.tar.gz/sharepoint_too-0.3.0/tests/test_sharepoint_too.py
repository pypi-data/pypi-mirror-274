import os
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv
from sharepoint_too import SharePointSession

load_dotenv()

# ------------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------------


@pytest.fixture()
def weblist_url():
    return os.getenv("SP_LIST_URL")


@pytest.fixture()
def list_title():
    return os.getenv("SP_LIST_TITLE")


@pytest.fixture()
def list_guid():
    return os.getenv("SP_LIST_GUID")


@pytest.fixture()
def list_item_type():
    return os.getenv("SP_LIST_ITEM_TYPE")


@pytest.fixture(scope="session")
def item():
    return {"id": None}


@pytest.fixture()
def sp():
    return SharePointSession(
        os.getenv("SP_BASE_URL"),
        username=f'{os.getenv("SP_DOMAIN")}\\{os.getenv("SP_USER")}',
        password=os.getenv("SP_PASSWORD"),
    )


# ------------------------------------------------------------------------------
# By GUID
# ------------------------------------------------------------------------------


def test_get_lists(sp, weblist_url):
    r = sp.get_lists(weblist_url)
    assert r.status_code == requests.codes.ok


def test_get_list_metadata_by_guid(sp, weblist_url, list_guid):
    r = sp.get_list_metadata_by_guid(weblist_url, list_guid=list_guid)
    assert r.status_code == requests.codes.ok


def test_get_list_items_by_guid(sp, weblist_url, list_guid):
    r = sp.get_list_items_by_guid(weblist_url, list_guid=list_guid)
    assert r.status_code == requests.codes.ok


def test_add_list_item_by_guid(sp, weblist_url, item, list_item_type, list_guid):
    add_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "ADDED remotely via rest api in python",
    }
    r = sp.add_list_item_by_guid(weblist_url, payload=add_payload, list_guid=list_guid)
    assert r.status_code == requests.codes.created

    # Set for use in future tests
    response = r.json()
    item["id"] = response["d"]["Id"]

    # Add this line to ensure that the item ID is not None
    assert item["id"] is not None


def test_get_list_entity_type_by_guid(sp, weblist_url, list_guid):
    r = sp.get_list_entity_type_by_guid(weblist_url, list_guid=list_guid)
    assert r.status_code == requests.codes.ok


def test_get_list_item_by_guid(sp, weblist_url, item, list_guid):
    r = sp.get_list_item_by_guid(weblist_url, list_guid=list_guid, item_id=item["id"])
    assert r.status_code == requests.codes.ok


def test_update_list_item_by_guid(sp, weblist_url, item, list_item_type, list_guid):
    update_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "UPDATED remotely via rest api in python",
    }
    r = sp.update_list_item_by_guid(
        weblist_url, item["id"], update_payload, list_guid=list_guid
    )
    assert r.status_code == requests.codes.no_content


def test_upload_by_guid(sp, weblist_url, item, list_guid):
    with Path("tests/nda.pdf").open("rb") as fh:
        r = sp.upload_by_guid(
            weblist_url, item["id"], fh.read(), "nda.pdf", list_guid=list_guid
        )
    assert r.status_code == requests.codes.ok


def test_delete_list_item_by_guid(sp, weblist_url, item, list_guid):
    r = sp.delete_list_item_by_guid(weblist_url, item["id"], list_guid=list_guid)
    assert r.status_code == requests.codes.ok


# ------------------------------------------------------------------------------
# By Title
# ------------------------------------------------------------------------------


def test_get_list_metadata_by_title(sp, weblist_url, list_title):
    r = sp.get_list_metadata_by_title(weblist_url, list_title=list_title)
    assert r.status_code == requests.codes.ok


def test_get_list_items_by_title(sp, weblist_url, list_title):
    r = sp.get_list_items_by_title(weblist_url, list_title=list_title)
    assert r.status_code == requests.codes.ok


def test_add_list_item_by_title(sp, weblist_url, item, list_item_type, list_title):
    add_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "ADDED remotely via rest api in python",
    }
    r = sp.add_list_item_by_title(
        weblist_url, payload=add_payload, list_title=list_title
    )
    assert r.status_code == requests.codes.created

    # Set for use in future tests
    response = r.json()
    item["id"] = response["d"]["Id"]


def test_get_list_entity_type_by_title(sp, weblist_url, list_title):
    r = sp.get_list_entity_type_by_title(weblist_url, list_title=list_title)
    assert r.status_code == requests.codes.ok


def test_get_list_item_by_title(sp, weblist_url, item, list_title):
    r = sp.get_list_item_by_title(
        weblist_url, list_title=list_title, item_id=item["id"]
    )
    assert r.status_code == requests.codes.ok


def test_update_list_item_by_title(sp, weblist_url, item, list_item_type, list_title):
    update_payload = {
        "__metadata": {"type": list_item_type},
        "Title": "UPDATED remotely via rest api in python",
    }
    r = sp.update_list_item_by_title(
        weblist_url, item["id"], update_payload, list_title=list_title
    )
    assert r.status_code == requests.codes.no_content


def test_upload_by_title(sp, weblist_url, item, list_title):
    with Path("tests/nda.pdf").open("rb") as fh:
        r = sp.upload_by_title(
            weblist_url, item["id"], fh.read(), "nda.pdf", list_title=list_title
        )
    assert r.status_code == requests.codes.ok


def test_delete_list_item_by_title(sp, weblist_url, item, list_title):
    r = sp.delete_list_item_by_title(weblist_url, item["id"], list_title=list_title)
    assert r.status_code == requests.codes.ok
