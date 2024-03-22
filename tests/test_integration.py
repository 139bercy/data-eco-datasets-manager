import pytest

from adapters.usecases import create_dataset, enrich_dataset
from core.models import Dataset
from infrastructure.exceptions import ExistingRecordError
from infrastructure.repositories import InMemoryDatasetRepository, TinyDbDatasetRepository

from tinydb import Query


def test_add_dataset_to_in_memory_repository(dataset_fixture):
    # Arrange
    repository = InMemoryDatasetRepository([])
    # Act
    create_dataset(repository=repository, values=dataset_fixture)
    # Assert
    assert repository.db[0].dataset_id == "my-dataset"


def test_add_base_dataset_to_tinydb_repository(dataset_fixture, tiny_db_repository):
    # Act
    create_dataset(repository=tiny_db_repository, values=dataset_fixture)
    # Assert
    query = Query()
    results = tiny_db_repository.db.search(query.dataset_id == "my-dataset")
    assert results[0]["dataset_id"] == "my-dataset"
    tiny_db_repository.clean()


def test_get_one_tiny_db_record(dataset_fixture, tiny_db_repository):
    # Arrange
    create_dataset(repository=tiny_db_repository, values=dataset_fixture)
    # Act
    result = tiny_db_repository.get_one(dataset_id="my-dataset")
    # Assert
    assert isinstance(result, Dataset)
    tiny_db_repository.clean()


def test_add_data_to_existing_dataset(dataset_fixture, dataset_update_fixture, tiny_db_repository):
    # Arrange
    dataset = create_dataset(repository=tiny_db_repository, values=dataset_fixture)
    # Act
    enrich_dataset(repository=tiny_db_repository, dataset=dataset, new_dataset=dataset_update_fixture)
    # Assert
    query = Query()
    results = tiny_db_repository.db.search(query.dataset_id == "my-dataset")
    assert results[0]["dataset_id"] == "my-dataset"
    assert results[0]["download_count"] == 100
    tiny_db_repository.clean()


def test_dataset_id_should_be_unique(dataset_fixture, tiny_db_repository):
    # Arrange & Act & Assert
    with pytest.raises(ExistingRecordError):
        create_dataset(repository=tiny_db_repository, values=dataset_fixture)
        create_dataset(repository=tiny_db_repository, values=dataset_fixture)
    # clean
    tiny_db_repository.clean()

