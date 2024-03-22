import json

import requests

from common import make_bytes_size_human_readable
from core.configuration import HEADERS, DOMAIN_NAME
from core.exceptions import HTTPError
from core.output import response_to_json, export


def query_ods(url: str, params: dict):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        output = response_to_json(response=response)
        return output
    else:
        raise HTTPError


def get_dataset_from_api(name: str, output: bool):
    url = f"{DOMAIN_NAME}/api/explore/v2.1/catalog/datasets/"
    params = {"where": f"dataset_id='{name}'", "include_app_metas": True}
    response = query_ods(url=url, params=params)
    if output:
        export(response=response, filename=f"data/dataset-sample.json")
    return response


def get_dataset_from_file():
    with open("data/dataset-sample.json", "r") as file:
        data = json.load(file)
        return data


def automation_api_dataset_dto(dataset: dict):
    dataset_report = {
        "created": dataset["created_at"],
        "updated": dataset["updated_at"],
        "dataset_id": dataset["dataset_id"],
        "title": dataset.get("metadata", {}).get("default", {}).get("title", {}).get("value", None),
        "publisher": dataset.get("metadata", {}).get("default", {}).get("publisher", {}).get("value", "Non renseigné"),
        "published": dataset["is_published"],
        "restricted": dataset["is_restricted"],
    }
    return dataset_report


def explore_api_dataset_dto(dataset: dict):
    records_size = dataset.get("metas", {}).get("processing", {}).get("records_size", None)
    dataset_report = {
        "download_count": dataset.get("metas", {}).get("explore", {}).get("download_count", None),
        "api_call_count": dataset.get("metas", {}).get("explore", {}).get("api_call_count", None),
        "popularity_score": dataset.get("metas", {}).get("explore", {}).get("popularity_score", None),
        "records_size": records_size,
        "size": make_bytes_size_human_readable(bytes_size=records_size),
        "records_count": dataset.get("metas", {}).get("default", {}).get("records_count", None),
    }
    return dataset_report
