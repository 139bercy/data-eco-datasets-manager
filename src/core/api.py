import requests

from core.configuration import HEADERS
from core.exceptions import HTTPError
from core.output import response_to_json


def query_ods(url: str, params: dict):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        output = response_to_json(response=response)
        return output
    else:
        raise HTTPError
