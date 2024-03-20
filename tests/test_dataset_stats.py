import json

import pytest

from adapters.usecases import create_dataset, enrich_dataset
from adapters.exceptions import DatasetInconsistencyError


def test_get_records_count(dataset_fixture):
    # Arrange
    base_dataset = create_dataset(**dataset_fixture)
    with open("tests/fixtures/dataset-sample-explore.json") as fixture:
        input = json.load(fixture)
        new_dataset = input["results"][0]
    # Act
    dataset = enrich_dataset(dataset=base_dataset, new_dataset=new_dataset)
    # Assert
    assert dataset.dataset_id == "my-dataset"
    assert dataset.download_count == 105


def test_enrich_dataset_names_should_be_consistent(dataset_fixture):
    # Arrange
    base_dataset = create_dataset(**dataset_fixture)
    with open("tests/fixtures/dataset-sample-explore.json") as fixture:
        input = json.load(fixture)
        new_dataset = input["results"][0]
        new_dataset["dataset_id"] = "asasasasa"
    # Act & Assert
    with pytest.raises(DatasetInconsistencyError):
        enrich_dataset(dataset=base_dataset, new_dataset=new_dataset)
