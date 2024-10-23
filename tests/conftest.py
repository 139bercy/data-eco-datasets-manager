import os

import pytest

from infrastructure.repositories import TinyDbDatasetRepository

os.environ["APP_ENV"] = "test"


@pytest.fixture
def dataset_fixture():
    return {
        "uid": "azerty",
        "created": "2024-01-01 10:00:00",
        "updated": "2024-01-02 12:00:00",
        "dataset_id": "my-dataset",
        "title": "My Dataset",
        "publisher": "My Organization",
        "published": True,
        "restricted": True,
    }


@pytest.fixture
def dataset_update_fixture():
    return {
        "dataset_id": "my-dataset",
        "metas": {
            "explore": {"download_count": 100, "api_call_count": 1000, "popularity_score": 4.2},
            "processing": {"records_size": 123456},
            "default": {"records_count": 400},
        },
        "attachments": [{"mimetype": "application/pdf", "title": "file-title.pdf"}],
    }


@pytest.fixture
def users_fixture():
    return {
        "username": "john.doe",
        "display_name": "John Doe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "gravatar_url": "//www.gravatar.com/avatar/a0572a91c8cbe0aac14e1edea26fa77a?d=mm&s=80",
        "account_type": "global",
        "permissions": [],
        "groups": [{"uid": "my-group"}],
        "is_active": True,
        "is_ods": False,
        "explore_limits": {},
        "management_limits": {},
        "identity_providers": [{"uid": "my-provider"}],
        "joined_at": "2024-01-01T12:00:00Z",
        "last_seen_at": "2024-01-01T12:00:00Z",
        "expires_at": None,
        "last_login_at": "2024-01-01T12:00:00Z",
        }


@pytest.fixture
def tiny_db_repository():
    try:
        return TinyDbDatasetRepository(name="db-test.json")
    finally:
        os.remove("db-test.json")
