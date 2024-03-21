import os

from tinydb import TinyDB, Query

from core.gateways import AbstractDatasetRepository
from core.models import Dataset
from infrastructure.exceptions import DatabaseDeletionError


class InMemoryDatasetRepository(AbstractDatasetRepository):
    def __init__(self, db):
        self.db = db

    def get_all(self):
        raise NotImplementedError

    def get_one(self, dataset_id: str):
        raise NotImplementedError

    def add(self, dataset):
        return self.db.append(dataset)

    def update(self, dataset_id, values):
        dataset = next((ds for ds in self.db if ds.dataset_id == dataset_id), None)
        if dataset:
            [setattr(dataset, key, value) for key, value in values.items()]
            return dataset
        else:
            raise ValueError("Dataset with ID {} not found".format(dataset_id))


class TinyDbDatasetRepository(AbstractDatasetRepository):
    def __init__(self, name):
        self.name = name
        self.db = TinyDB(name, indent=2, ensure_ascii=False)

    def get_all(self):
        raise NotImplementedError

    def get_one(self, dataset_id: str):
        query = Query()
        result = self.db.search(query.dataset_id == dataset_id)[0]
        dataset = Dataset(**result)
        return dataset

    def add(self, dataset):
        self.db.insert(dataset.__dict__)

    def update(self, dataset_id: str, values: dict) -> None:
        query = Query()
        self.db.update(values, query.dataset_id == dataset_id)

    def clean(self):
        if os.environ["APP_ENV"] == "test":
            os.remove(self.name)
        else:
            raise DatabaseDeletionError
