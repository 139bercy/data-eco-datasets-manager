import json

import requests

from core.configuration import HEADERS
from core.exceptions import HTTPError
from core.output import response_to_json, export


def query_ods(url: str, params: dict):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        output = response_to_json(response=response)
        return output
    else:
        raise HTTPError


def get_dataset_from_api(name, output):
    url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
    params = {"where": f"dataset_id='{name}'", "include_app_metas": True}
    response = query_ods(url=url, params=params)
    if output:
        export(response=response, filename=f"data/dataset-sample.json")


def get_dataset_from_file():
    with open("data/dataset-sample.json", "r") as file:
        data = json.load(file)
        return data
