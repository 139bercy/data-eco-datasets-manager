from adapters.usecases import create_dataset
from infrastructure.repositories import InMemoryDatasetRepository, TinyDbDatasetRepository

from tinydb import Query


def test_add_dataset_to_in_memory_repository(dataset_fixture):
    # Arrange
    repository = InMemoryDatasetRepository([])
    # Act
    create_dataset(repository=repository, values=dataset_fixture)
    # Assert
    assert repository.db[0].dataset_id == "my-dataset"


def test_add_dataset_to_tinydb_repository(dataset_fixture, tiny_db_name):
    # Arrange
    repository = TinyDbDatasetRepository(name=tiny_db_name)
    # Act
    create_dataset(repository=repository, values=dataset_fixture)
    # Assert
    query = Query()
    results = repository.db.search(query.dataset_id == 'my-dataset')
    assert results[0]["dataset_id"] == "my-dataset"
    repository.clean()
