import json
from collections import defaultdict
from operator import itemgetter

import requests

from common import make_bytes_size_human_readable
from core.configuration import HEADERS, DOMAIN_NAME
from core.exceptions import HTTPError
from core.output import response_to_json, to_json, pprint

import mimetypes


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
        to_json(response=response, filename=f"data/{name}.json")
    return response


def get_dataset_from_automation_api(dataset_uid: str, output: bool):
    url = f"{DOMAIN_NAME}/api/automation/v1.0/datasets/{dataset_uid}"
    response = query_ods(url=url, params={})
    if output:
        to_json(response=response, filename=f"data/{response['dataset_id']}.json")
    return response


def get_dataset_from_file():
    with open("data/dataset-sample.json", "r") as file:
        data = json.load(file)
        return data


def get_attachments_files_extensions(files):
    extensions = defaultdict(int)
    for file in files:
        extension = mimetypes.guess_extension(file["mimetype"]).replace(".", "")
        extensions[extension] += 1
    unpacked = [{"extension": key, "value": value} for key, value in dict(extensions).items()] if len(extensions) >= 1 else None
    result = sorted(unpacked, key=itemgetter("extension"), reverse=False) if unpacked else None
    return result


def automation_api_dataset_dto(dataset: dict):
    dataset_report = {
        "uid": dataset["uid"],
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
        "attachments": get_attachments_files_extensions(dataset.get("attachments", None)),
        "download_count": dataset.get("metas", {}).get("explore", {}).get("download_count", None),
        "api_call_count": dataset.get("metas", {}).get("explore", {}).get("api_call_count", None),
        "popularity_score": dataset.get("metas", {}).get("explore", {}).get("popularity_score", None),
        "records_size": records_size,
        "size": make_bytes_size_human_readable(bytes_size=records_size),
        "records_count": dataset.get("metas", {}).get("default", {}).get("records_count", None),
        "link": f"https://data.economie.gouv.fr/explore/dataset/{dataset['dataset_id']}",
    }
    return dataset_report
