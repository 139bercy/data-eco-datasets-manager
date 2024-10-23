import csv

from core.api import query_ods
from core.configuration import DOMAIN_NAME

from core.gateways import AbstractDatasetRepository
from datasets.api import get_dataset_from_api


class DatasetCsvRepository(AbstractDatasetRepository):
    path = "data/"

    def __init__(self, filename):
        self.filename = filename

    @property
    def filepath(self):
        return f"{self.path}{self.filename}"

    def all(self):
        with open(self.filepath, "r") as file:
            reader = csv.DictReader(file, delimiter=";")
            return [row for row in reader]

    def one(self, dataset_id):
        with open(self.filepath, "r") as file:
            reader = csv.DictReader(file)
            return next((row for row in reader if row["dataset_id"] == dataset_id), None)

    def add(self, dataset):
        raise NotImplementedError

    def update(self, dataset_id: str, values: dict) -> None:
        raise NotImplementedError

    def upsert(self, dataset):
        raise NotImplementedError


class DatasetApiRepository(AbstractDatasetRepository):
    def upsert(self, dataset):
        raise NotImplementedError

    def all(self):
        response = query_ods(f"{DOMAIN_NAME}/api/automation/v1.0/datasets/", params={"limit": 1000})
        return response

    def one(self, dataset_id):
        return get_dataset_from_api(dataset_id, False)

    def add(self, dataset):
        raise NotImplementedError

    def update(self, dataset_id: str, values: dict) -> None:
        raise NotImplementedError
