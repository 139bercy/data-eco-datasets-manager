import json

import pytest

from adapters.api import explore_api_dataset_dto
from adapters.usecases import create_dataset, enrich_dataset
from adapters.exceptions import DatasetInconsistencyError
from common import make_bytes_size_human_readable
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
    assert dataset.size == "123.46 Ko"
    assert dataset.records_count == 400


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


def test_explore_empty_values_should_return_none():
    # Arrange
    expected = {
        "api_call_count": None,
        "download_count": None,
        "popularity_score": None,
        "records_size": None,
        "size": None,
        "records_count": None,
    }
    # Act
    result = explore_api_dataset_dto({})
    # Assert
    assert result == expected


def test_should_render_human_readable_sizes_ko():
    # Arrange
    size = 1234
    # Act
    result = make_bytes_size_human_readable(bytes_size=size)
    # Assert
    assert result == "1.23 Ko"


def test_should_render_human_readable_sizes_mo():
    # Arrange
    size = 12345678
    # Act
    result = make_bytes_size_human_readable(bytes_size=size)
    # Assert
    assert result == "12.35 Mo"


def test_should_render_human_readable_sizes_go():
    # Arrange
    size = 12345678910
    # Act
    result = make_bytes_size_human_readable(bytes_size=size)
    # Assert
    assert result == "12.35 Go"
