import requests

from core.configuration import DOMAIN_NAME, HEADERS


def unpublish(dataset_uid):
    url = f"{DOMAIN_NAME}/api/automation/v1.0/datasets/{dataset_uid}/unpublish"
    response = requests.post(url=url, headers=HEADERS)
    print(f"Unpublish dataset {dataset_uid} : {response.status_code} : {response.text}")
    return response.status_code


def publish(dataset_uid):
    url = f"{DOMAIN_NAME}/api/automation/v1.0/datasets/{dataset_uid}/publish"
    response = requests.post(url=url, headers=HEADERS)
    print(f"Publish dataset {dataset_uid} : {response.status_code} : {response.text}")
    return response.status_code
