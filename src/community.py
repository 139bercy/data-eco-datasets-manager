import json

import requests
from core.configuration import HEADERS


def add_community_custom_view(dataset_uid):
    html_payload = {"value": read_file("src/adapters/assets/community.html")}
    css_payload = {"value": read_file("src/adapters/assets/community.css")}
    html_custom_view_exists = check_html_custom_view_exists(dataset_uid=dataset_uid)
    css_custom_view_exists = check_css_custom_view_exists(dataset_uid=dataset_uid)

    if html_custom_view_exists and css_custom_view_exists:
        print("Abord: custom view already exists. ")
        return

    add_html_custom_view(dataset_uid=dataset_uid, html_payload=html_payload)
    add_css_custom_view(dataset_uid=dataset_uid, css_payload=css_payload)
    activate_custom_view(dataset_uid=dataset_uid)
    add_title_to_custom_view(dataset_uid=dataset_uid)
    add_icon_to_custom_view(dataset_uid=dataset_uid)
    publish_metadata(dataset_uid=dataset_uid)


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def check_html_custom_view_exists(dataset_uid):
    response = requests.get(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/metadata/visualization/custom_view_html",
        headers=HEADERS,
    )
    if not response.json().get("value"):
        return False
    return True


def check_css_custom_view_exists(dataset_uid):
    response = requests.get(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/metadata/visualization/custom_view_css",
        headers=HEADERS,
    )
    if not response.json().get("value"):
        return False
    return True


def add_html_custom_view(dataset_uid, html_payload):
    response = requests.put(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/metadata/visualization/custom_view_html",
        json=html_payload,
        headers=HEADERS,
    )
    print("Add HTML custom view", json.loads(response.text))


def add_css_custom_view(dataset_uid, css_payload):
    response = requests.put(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/metadata/visualization/custom_view_css",
        json=css_payload,
        headers=HEADERS,
    )
    print("Add CSS custom view", json.loads(response.text))


def activate_custom_view(dataset_uid):
    payload = {"value": True}
    response = requests.put(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/metadata/visualization/custom_view_enabled",
        json=payload,
        headers=HEADERS,
    )
    print("Activate custom view", json.loads(response.text))


def add_title_to_custom_view(dataset_uid):
    title_playload = {"value": "Communauté"}
    response = requests.put(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/metadata/visualization/custom_view_title",
        json=title_playload,
        headers=HEADERS,
    )
    print("Add Title", json.loads(response.text))


def add_icon_to_custom_view(dataset_uid):
    icon_payload = {"value": "users"}
    response = requests.put(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/metadata/visualization/custom_view_icon",
        json=icon_payload,
        headers=HEADERS,
    )
    print("Add Icon", json.loads(response.text))


def publish_metadata(dataset_uid):
    response = requests.post(
        f"https://data.economie.gouv.fr/api/automation/v1.0/datasets/{dataset_uid}/publish_metadata", headers=HEADERS
    )
    print("Publish", json.loads(response.text))
