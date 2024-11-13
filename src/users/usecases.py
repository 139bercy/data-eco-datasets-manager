import requests

from core.configuration import DOMAIN_NAME, HEADERS
from core.output import pprint
from users.api import user_dto
from users.models import User


def import_user(repository, user: dict):
    dto = user_dto(user=user)
    user = User.create(**dto)
    repository.upsert(user=user)
    return user


def create_user(email: str, groups: list):
    url = f"{DOMAIN_NAME}/api/automation/v1.0/users/invite/"
    response = requests.post(url=url, headers=HEADERS, json={"email": email, "groups": groups})
    if response.status_code == 201:
        print("Success!")
    pprint(f"Code: {response.status_code}\n{response.json()}")


def add_user_to_group(group_id: str, username: str):
    url = f"{DOMAIN_NAME}/api/automation/v1.0/groups/{group_id}/users/"
    response = requests.post(url=url, headers=HEADERS, json={"username": username})
    print(response.status_code)
    pprint(response.json())

