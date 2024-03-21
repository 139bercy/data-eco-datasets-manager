import csv

from adapters.api import query_ods, get_dataset_from_api
from core.configuration import DOMAIN_NAME

from core.gateways import AbstractDatasetRepository


class DatasetCsvRepository(AbstractDatasetRepository):
    path = "data/"

    def __init__(self, filename):
        self.filename = filename

    @property
    def filepath(self):
        return f"{self.path}{self.filename}"

    def get_all(self):
        with open(self.filepath, "r") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def get_one(self, dataset_id):
        with open(self.filepath, "r") as file:
            reader = csv.DictReader(file)
            return next((row for row in reader if row["dataset_id"] == dataset_id), None)

    def add(self, dataset):
        raise NotImplementedError

    def update(self, dataset_id: str, values: dict) -> None:
        raise NotImplementedError


class DatasetApiRepository(AbstractDatasetRepository):
    def get_all(self):
        response = query_ods(f"{DOMAIN_NAME}/api/automation/v1.0/datasets/", params={"limit": 1000})
        return response

    def get_one(self, dataset_id):
        return get_dataset_from_api(dataset_id, False)

    def add(self, dataset):
        raise NotImplementedError

    def update(self, dataset_id: str, values: dict) -> None:
        raise NotImplementedError
