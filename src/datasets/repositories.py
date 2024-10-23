import os

from tinydb import TinyDB, Query

from core.gateways import AbstractDatasetRepository
from core.models import Dataset
from core.exceptions import DatabaseDeletionError, ExistingRecordError
from core.builder import TinyDBQueryBuilder


def type_value(value):
    try:
        return int(value)
    except ValueError:
        return value


class InMemoryDatasetRepository(AbstractDatasetRepository):
    def __init__(self, db):
        self.db = db

    def all(self):
        raise NotImplementedError

    def one(self, dataset_id: str):
        raise NotImplementedError

    def add(self, dataset: Dataset):
        return self.db.append(dataset)

    def update(self, dataset_id: str, values: dict):
        dataset = next((ds for ds in self.db if ds.dataset_id == dataset_id), None)
        if dataset:
            [setattr(dataset, key, value) for key, value in values.items()]
            return dataset
        else:
            raise ValueError("Dataset with ID {} not found".format(dataset_id))

    def upsert(self, dataset):
        try:
            self.add(dataset)
        except ExistingRecordError:
            self.update(dataset.dataset_id, dataset.__dict__)


class TinyDbDatasetRepository(AbstractDatasetRepository):
    def __init__(self, name):
        self.name = name
        self.db = TinyDB(name, indent=2, ensure_ascii=False)
        self.builder = TinyDBQueryBuilder(db=self.db)
        self.datasets = self.db.table("datasets")

    def is_unique(self, dataset_id):
        index = {value["dataset_id"] for value in self.datasets.all()}
        result = next((dsid for dsid in index if dsid == dataset_id), None)
        if result:
            return False
        return True

    def all(self):
        return self.datasets.all()

    def one(self, dataset_id: str):
        query = Query()
        result = self.datasets.search(query.dataset_id == dataset_id)
        if len(result) != 0:
            dataset = Dataset(**result[0])
            return dataset

    def search(self, field, value):
        query = Query()
        new_value = type_value(value=value)
        if type(new_value) == bool or type(new_value) == int:
            results = self.datasets.search(getattr(query, field) == new_value)
        else:
            results = self.datasets.search(query[field].search(new_value))
        if len(results) >= 1:
            return results
        return None

    def query(self):
        query = self.builder.build_query()
        if not query:
            return self.datasets.all()
        return self.datasets.search(query)

    def add(self, dataset: Dataset):
        if self.is_unique(dataset_id=dataset.dataset_id):
            self.datasets.insert(dataset.__dict__)
        else:
            raise ExistingRecordError

    def upsert(self, dataset: Dataset):
        try:
            self.add(dataset)
        except ExistingRecordError:
            self.update(dataset.dataset_id, dataset.__dict__)

    def update(self, dataset_id: str, values: dict) -> None:
        query = Query()
        self.datasets.update(values, query.dataset_id == dataset_id)

    def clean(self):
        if os.environ["APP_ENV"] == "test":
            os.remove(self.name)
        else:
            raise DatabaseDeletionError
