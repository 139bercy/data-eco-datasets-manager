import os

from tinydb import TinyDB, Query

from core.gateways import AbstractDatasetRepository
from core.models import Dataset
from infrastructure.exceptions import DatabaseDeletionError, ExistingRecordError
from infrastructure.builder import TinyDBQueryBuilder


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

    def is_unique(self, dataset_id):
        index = {value["dataset_id"] for value in self.db.all()}
        result = next((dsid for dsid in index if dsid == dataset_id), None)
        if result:
            return False
        return True

    def get_all(self):
        raise NotImplementedError

    def get_one(self, dataset_id: str):
        query = Query()
        result = self.db.search(query.dataset_id == dataset_id)[0]
        dataset = Dataset(**result)
        return dataset

    def search(self, field, value):
        query = Query()
        if type(value) == bool:
            results = self.db.search((getattr(query, field) == value))
        else:
            results = self.db.search(query[field].search(value))
        if len(results) >= 1 :
            return results
        return None

    def query(self, query=None):
        if not query:
            return self.db.all()
        return self.db.search(query)

    def add(self, dataset):
        if self.is_unique(dataset_id=dataset.dataset_id):
            self.db.insert(dataset.__dict__)
        else:
            raise ExistingRecordError

    def update(self, dataset_id: str, values: dict) -> None:
        query = Query()
        self.db.update(values, query.dataset_id == dataset_id)

    def clean(self):
        if os.environ["APP_ENV"] == "test":
            os.remove(self.name)
        else:
            raise DatabaseDeletionError
