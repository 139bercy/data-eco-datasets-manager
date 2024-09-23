import csv

import requests

from core.configuration import DOMAIN_NAME, HEADERS
from core.output import pprint


def get_users():
    base_url = f"{DOMAIN_NAME}/api/automation/v1.0/users/export/"
    response = requests.get(url=base_url, headers=HEADERS)
    reader = csv.DictReader(response.content.decode("utf-8").splitlines(), dialect="unix")
    data = [row for row in reader]
    return data


def get_groups():
    base_url = f"{DOMAIN_NAME}/api/automation/v1.0/groups/?limit=100&sort=group__title"
    response = requests.get(url=base_url, headers=HEADERS)
    result = response.json()
    data = result["results"]
    print("Groups total count", result["total_count"])
    return data


def update_one_group_permissions(group_id: str, title: str, permissions: list):
    base_url = f"{DOMAIN_NAME}/api/automation/v1.0/groups/{group_id}/"
    response = requests.put(url=base_url, headers=HEADERS, data={"permissions": permissions, "title": title})
    pprint(response.json())
