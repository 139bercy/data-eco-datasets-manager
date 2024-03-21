import json

import pytest

from adapters.usecases import create_dataset, enrich_dataset
from adapters.exceptions import DatasetInconsistencyError
from infrastructure.repositories import InMemoryDatasetRepository


def test_should_add_data_to_existing_dataset(dataset_fixture):
    # Arrange
    repository = InMemoryDatasetRepository([])
    base_dataset = create_dataset(repository=repository, values=dataset_fixture)
    with open("tests/fixtures/dataset-sample-explore.json") as fixture:
        input = json.load(fixture)
        new_dataset = input["results"][0]
    # Act
    dataset = enrich_dataset(repository=repository, dataset=base_dataset, new_dataset=new_dataset)
    # Assert
    assert dataset.dataset_id == "my-dataset"
    assert dataset.download_count == 100
    assert dataset.api_call_count == 1000
    assert dataset.popularity_score == 4.2
    assert dataset.records_size == 123456


def test_enrich_dataset_names_should_be_consistent(dataset_fixture):
    # Arrange
    repository = InMemoryDatasetRepository([])
    base_dataset = create_dataset(repository=repository, values=dataset_fixture)
    with open("tests/fixtures/dataset-sample-explore.json") as fixture:
        input = json.load(fixture)
        new_dataset = input["results"][0]
        new_dataset["dataset_id"] = "asasasasa"
    # Act & Assert
    with pytest.raises(DatasetInconsistencyError):
        enrich_dataset(repository=repository, dataset=base_dataset, new_dataset=new_dataset)
