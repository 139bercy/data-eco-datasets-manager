import csv

import requests

from datetime import datetime

from common import format_filename
from core.configuration import DOMAIN_NAME, HEADERS
from core.output import to_csv


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
