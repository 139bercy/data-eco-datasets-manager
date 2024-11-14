import copy

from core.exceptions import DatasetInconsistencyError
from core.models import Dataset
from core.output import sort_by_field, output_results
from datasets.api import explore_api_dataset_dto


def create_dataset(repository, values) -> Dataset:
    dataset = Dataset.create(**values)
    repository.upsert(dataset)
    return dataset


def enrich_dataset(repository, dataset: Dataset, new_dataset: dict) -> Dataset:
    dto = explore_api_dataset_dto(new_dataset)
    if dataset.dataset_id != new_dataset["dataset_id"]:
        raise DatasetInconsistencyError
    dataset_copy = copy.deepcopy(dataset)
    dataset_copy.update(**dto)
    repository.update(dataset.dataset_id, dto)
    return dataset_copy


def search_resources(chain: str, detail: bool, field: str, repository, sort: str):
    data = repository.search(field=field, value=chain)
    results = sort_by_field(data=data, field=sort)
    output_results(results=results, detail=detail)
    return results
