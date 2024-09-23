import csv

import requests

from datetime import datetime

from common import format_filename
from core.configuration import DOMAIN_NAME, HEADERS
from core.output import csv_format_datasets_list


def get_users():
    base_url = f"{DOMAIN_NAME}/api/automation/v1.0/users/export/"
    response = requests.get(url=base_url, headers=HEADERS)
    reader = csv.DictReader(response.content.decode('utf-8').splitlines(), dialect='unix')
    data = [row for row in reader]
    filename = format_filename(f"users.csv", ".")
    csv_format_datasets_list(report=data, filename=filename, headers=data[0].keys())


def get_groups():
    base_url = f"{DOMAIN_NAME}/api/automation/v1.0/groups/?limit=100&sort=group__title"
    headers = ["title", "description", "permissions", "uid", "management_limits", "explore_limits", "user_count", "created_at", "updated_at"]

    response = requests.get(url=base_url, headers=HEADERS)
    result = response.json()
    data = result["results"]
    print("Groups total count", result["total_count"])

    filename = format_filename(f"groups.csv", ".")
    csv_format_datasets_list(report=data, filename=filename, headers=headers)
