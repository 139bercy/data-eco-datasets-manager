import copy

from adapters.api import explore_api_dataset_dto
from adapters.exceptions import DatasetInconsistencyError
from common import format_filename
from core.models import Dataset
from core.output import sort_by_field, choose_headers, to_csv, output_results


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


def search_resources(chain, detail, export, field, header, repository, role, sort):
    data = repository.search(field=field, value=chain)
    results = sort_by_field(data=data, field=sort)
    headers = list(header) if len(header) != 0 else choose_headers(role=role)
    output_results(results=results, detail=detail)
    if export:
        output = format_filename(f"datasets-{field}-{chain}.csv", "data")
        to_csv(report=results, filename=output, headers=headers)
