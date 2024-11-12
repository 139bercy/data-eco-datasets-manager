import os

from users.repositories import InMemoryUsersRepository, TinyDbUserRepository
from users.usecases import import_user


def test_import_user(users_fixture):
    # Arrange
    repository = InMemoryUsersRepository([])
    # Act
    user = import_user(repository=repository, user=users_fixture)
    # Assert
    assert len(repository.db) == 1
    assert user.buid == "c0c10d06"
    

def test_update_user(users_fixture):
    # Arrange
    repository = InMemoryUsersRepository([])
    import_user(repository=repository, user=users_fixture)
    updated = {**users_fixture, "last_seen_at": "2024-01-02T12:00:00Z"}
    # Act
    repository.update(username="john.doe", values=updated)
    # Assert
    user = repository.one(username="john.doe")
    assert len(repository.db) == 1
    assert user.buid == "c0c10d06"
    assert user.last_seen_at == "2024-01-02T12:00:00Z"


def test_upsert_user(users_fixture):
    # Arrange
    repository = InMemoryUsersRepository([])
    user = import_user(repository=repository, user=users_fixture)
    user.update(last_seen_at="2024-01-02T12:00:00Z")
    # Act
    repository.upsert(user=user)
    # Assert
    user = repository.one(username="john.doe")
    assert len(repository.db) == 1
    assert user.last_seen_at == "2024-01-02T12:00:00Z"


def test_import_user_on_tinydb(users_fixture):
    # Arrange
    repository = TinyDbUserRepository("db-test.json")
    # Act
    user = import_user(repository=repository, user=users_fixture)
    # Assert
    assert len(repository.all()) == 1
    assert user.buid == "c0c10d06"
    os.remove("db-test.json")


def test_update_user_on_tinydb(users_fixture):
    # Arrange
    repository = TinyDbUserRepository("db-test.json")
    import_user(repository=repository, user=users_fixture)
    updated = {"last_seen_at": "2024-01-02T12:00:00Z"}
    # Act
    repository.update(username="john.doe", values=updated)
    # Assert
    user = repository.one(username="john.doe")
    assert user.buid == "c0c10d06"
    assert user.last_seen_at == "2024-01-02T12:00:00Z"
    os.remove("db-test.json")


def test_upsert_user_on_tinydb(users_fixture):
    # Arrange
    repository = TinyDbUserRepository("db-test.json")
    user = import_user(repository=repository, user=users_fixture)
    user.update(last_seen_at="2024-01-02T12:00:00Z")
    # Act
    repository.upsert(user=user)
    # Assert
    user = repository.one(username="john.doe")
    assert user.buid == "c0c10d06"
    assert user.last_seen_at == "2024-01-02T12:00:00Z"
    os.remove("db-test.json")
