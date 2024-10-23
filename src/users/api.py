import requests

from core.configuration import DOMAIN_NAME, HEADERS


def get_all_users_from_api():
    base_url = f"{DOMAIN_NAME}/api/automation/v1.0/users/"
    response = requests.get(url=base_url, headers=HEADERS, params={"limit": 1000})
    raw = response.json()
    results = raw["results"]
    return results


def user_dto(user: dict):
    return {
        "username": user.get("username"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "email": user.get("email"),
        "permissions": user.get("permissions"),
        "groups": user.get("groups"),
        "is_active": user.get("is_active"),
        "joined_at": user.get("joined_at"),
        "last_seen_at": user.get("last_seen_at"),
        "last_login_at": user.get("last_login_at"),
    }
