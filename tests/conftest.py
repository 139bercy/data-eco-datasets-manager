import pytest


@pytest.fixture
def dataset_fixture():
    return {
        "created": "2024-01-01 10:00:00",
        "updated": "2024-01-02 12:00:00",
        "dataset_id": "my-dataset",
        "title": "My Dataset",
        "publisher": "My Organization",
        "published": True,
        "restricted": True,
    }


