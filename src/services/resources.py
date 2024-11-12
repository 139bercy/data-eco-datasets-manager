import requests

from core.configuration import HEADERS, DOMAIN_NAME
from core.output import pprint


def create_group(title: str, permissions: list):
    url = f"{DOMAIN_NAME}/api/automation/v1.0/groups/"
    response = requests.post(url=url, headers=HEADERS, json={"title": title, "permissions": permissions})
    if response.status_code == 201:
        print("Success!")
    pprint(response.json())
