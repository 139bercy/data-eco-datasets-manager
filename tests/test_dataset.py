import requests_mock

from core.configuration import DOMAIN_NAME
from adapters.primaries import DatasetCsvRepository, DatasetApiRepository


def test_should_retrieve_a_list_of_datasets_from_csv():
    # Arrange
    repository = DatasetCsvRepository("datasets.csv")
    repository.path = "tests/fixtures/"
    # Act
    datasets = repository.get_all()
    # Assert
    assert len(datasets) == 3


def test_should_retrieve_one_dataset_from_csv():
    # Arrange
    repository = DatasetCsvRepository("datasets.csv")
    repository.path = "tests/fixtures/"
    dataset_id = "test-dataset-1"
    # Act
    dataset = repository.get_one(dataset_id=dataset_id)
    # Assert
    assert dataset["dataset_id"] == dataset_id


def test_should_retrieve_a_list_of_datasets_from_api():
    # Arrange
    repository = DatasetApiRepository()
    with open("tests/fixtures/datasets.json", "r") as file:
        content = file.read()
    # Act
    with requests_mock.Mocker() as m:
        m.get(f"{DOMAIN_NAME}/api/automation/v1.0/datasets/", text=content)
        datasets = repository.get_all()
    # Assert
    assert datasets["total_count"] == 3


def test_should_retrieve_one_dataset_from_api():
    # Arrange
    repository = DatasetApiRepository()
    with open("tests/fixtures/dataset.json", "r") as file:
        content = file.read()
    # Act
    with requests_mock.Mocker() as m:
        m.get(f"{DOMAIN_NAME}/api/explore/v2.1/catalog/datasets/", text=content)
        datasets = repository.get_one("test-dataset-1")
    # Assert
    assert datasets["total_count"] == 1
