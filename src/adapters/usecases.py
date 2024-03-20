import copy

from adapters.api import explore_api_dataset_dto
from adapters.exceptions import DatasetInconsistencyError
from core.models import Dataset


def create_dataset(repository, values) -> Dataset:
    dataset = Dataset.create(**values)
    repository.add(dataset)
    return dataset


def enrich_dataset(dataset: Dataset, new_dataset: dict) -> Dataset:
    dto = explore_api_dataset_dto(new_dataset)
    if dataset.dataset_id != new_dataset["dataset_id"]:
        raise DatasetInconsistencyError
    dataset_copy = copy.deepcopy(dataset)
    dataset_copy.update(**{"download_count": dto["download_count"]})
    return dataset_copy
