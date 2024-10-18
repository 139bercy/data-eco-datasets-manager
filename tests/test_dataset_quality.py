import pytest

from services.quality import (
    get_global_quality_score,
    get_metadata_quality_score,
    get_dataset_quality_score,
)


@pytest.fixture
def dataset():
    data = {
        "total_count": 1,
        "results": [
            {
                "dataset_id": "test_dataset",
                "metas": {
                    "description": {"title": "Dataset title", "description": None},
                    "default": {"field1": True, "field2": None},
                    "dcat": {"field1": True, "field2": True},
                },
            }
        ],
    }
    return data


def test_get_dataset_quality_report(dataset):
    # Act
    report = get_dataset_quality_score(data=dataset)
    # Assert
    assert report["quality_score"] == 75


def test_get_dataset_quality_report_without_dcat(dataset):
    # Act
    report = get_dataset_quality_score(data=dataset, dcat=False, pprint=False)
    # Assert
    assert report["dcat_score"] is None
    assert report["quality_score"] == 50


def test_dataset_is_empty_should_give_default_report():
    # Arrange
    dataset = {"total_count": 0, "results": []}
    # Act
    report = get_dataset_quality_score(data=dataset, pprint=False)
    assert report == {"description_score": None, "default_score": None, "dcat_score": None, "quality_score": None}


def test_calculate_average_score():
    # Arrange
    metrics = [10, 12, 14]
    # Act
    average = get_global_quality_score(metrics=metrics)
    # Assert
    assert average == 12


def test_calculate_average_score_with_wrong_value():
    # Arrange
    metrics = ["N/A", 10, 14]
    # Act
    average = get_global_quality_score(metrics=metrics)
    # Assert
    assert average == 12


def test_calculate_metadata_quality_score():
    # Arrange
    data = {"results": [{"dataset_id": "test_dataset", "metas": {"default": {"field1": True, "field2": None}}}]}
    # Act
    report = get_metadata_quality_score(data, "default", pprint=False)
    assert report["score"] == 50


def test_calculate_metadata_field_is_false():
    # Arrange
    data = {"results": [{"dataset_id": "test_dataset", "metas": {"default": {"field1": False, "field2": None}}}]}
    # Act
    report = get_metadata_quality_score(data, "default", pprint=False)
    # Assert
    assert report["score"] == 50


def test_calculate_metadata_is_empty():
    # Arrange
    data = {"results": [{"dataset_id": "test_dataset", "metas": {"default": {}}}]}
    # Act
    report = get_metadata_quality_score(data, "default", pprint=False)
    # Assert
    assert report["score"] is None
