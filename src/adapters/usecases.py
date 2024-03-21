import copy

from adapters.api import explore_api_dataset_dto
from adapters.exceptions import DatasetInconsistencyError
from core.models import Dataset


def create_dataset(repository, values) -> Dataset:
    dataset = Dataset.create(**values)
    repository.add(dataset)
    return dataset


def enrich_dataset(repository, dataset: Dataset, new_dataset: dict) -> Dataset:
    dto = explore_api_dataset_dto(new_dataset)
    if dataset.dataset_id != new_dataset["dataset_id"]:
        raise DatasetInconsistencyError
    dataset_copy = copy.deepcopy(dataset)
    dataset_copy.update(**dto)
    repository.update(dataset.dataset_id, dto)
    return dataset_copy
