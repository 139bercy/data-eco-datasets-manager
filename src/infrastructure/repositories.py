import os

from tinydb import TinyDB

from core.gateways import AbstractDatasetRepository


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
    def __init__(self):
        self.db = TinyDB('db-test.json', indent=2)

    def get_all(self):
        raise NotImplementedError

    def get_one(self, dataset_id: str):
        raise NotImplementedError

    def add(self, dataset):
        self.db.insert(dataset.__dict__)

    def clean(self):
        os.remove("db-test.json")
