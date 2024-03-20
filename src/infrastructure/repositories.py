import os

from tinydb import TinyDB

from core.gateways import AbstractDatasetRepository
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


class TinyDbDatasetRepository(AbstractDatasetRepository):
    def __init__(self, name):
        self.name = name
        self.db = TinyDB(name, indent=2)

    def get_all(self):
        raise NotImplementedError

    def get_one(self, dataset_id: str):
        raise NotImplementedError

    def add(self, dataset):
        self.db.insert(dataset.__dict__)

    def clean(self):
        if os.environ["APP_ENV"] == "test":
            os.remove(self.name)
        else:
            raise DatabaseDeletionError
