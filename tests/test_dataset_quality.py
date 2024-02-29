import pytest

from src.quality import (
    get_global_quality_ratio,
    get_metadata_quality_ratio,
    get_dataset_quality_ratio,
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
    report = get_dataset_quality_ratio(data=dataset)
    # Assert
    assert report["quality_ratio"] == 75


def test_get_dataset_quality_report_without_dcat(dataset):
    # Act
    report = get_dataset_quality_ratio(data=dataset, dcat=False)
    # Assert
    assert report["dcat_metadata_percent"] == "N/A"
    assert report["quality_ratio"] == 50


def test_dataset_is_empty_should_give_default_report():
    # Arrange
    dataset = {"total_count": 0, "results": []}
    # Act
    report = get_dataset_quality_ratio(data=dataset)
    assert report == {
        "description_metadata_percent": "N/A",
        "default_metadata_percent": "N/A",
        "dcat_metadata_percent": "N/A",
        "quality_ratio": "N/A",
    }


def test_calculate_average_ratio():
    # Arrange
    metrics = [10, 12, 14]
    # Act
    average = get_global_quality_ratio(metrics=metrics)
    # Assert
    assert average == 12


def test_calculate_average_ratio_with_wrong_value():
    # Arrange
    metrics = ["N/A", 10, 14]
    # Act
    average = get_global_quality_ratio(metrics=metrics)
    # Assert
    assert average == 12


def test_calculate_metadata_quality_ratio():
    # Arrange
    data = {
        "results": [
            {
                "dataset_id": "test_dataset",
                "metas": {"default": {"field1": True, "field2": None}},
            }
        ]
    }
    # Act
    report = get_metadata_quality_ratio(data, "default", pprint=True)
    assert report["ratio"] == 50


def test_calculate_metadata_field_is_false():
    # Arrange
    data = {
        "results": [
            {
                "dataset_id": "test_dataset",
                "metas": {"default": {"field1": False, "field2": None}},
            }
        ]
    }
    # Act
    report = get_metadata_quality_ratio(data, "default", pprint=True)
    # Assert
    assert report["ratio"] == 50


def test_calculate_metadata_is_empty():
    # Arrange
    data = {
        "results": [
            {
                "dataset_id": "test_dataset",
                "metas": {"default": {}},
            }
        ]
    }
    # Act
    report = get_metadata_quality_ratio(data, "default", pprint=True)
    # Assert
    assert report["ratio"] == "N/A"


# def test_get_report():
#     # Arrange
#     data = {
#         "results": [
#             {
#                 "dataset_id": "test_dataset",
#                 "metadata": {
#                     "description": {
#                         "field1": True,
#                         "field2": None
#                     },
#                     "default": {
#                         "field1": True,
#                         "field2": None
#                     },
#                     "dcat": {
#                         "field1": True,
#                         "field2": None
#                     },
#                 }
#             }
#
#         ]
#     }
#     # Act
#     average = get_report(data=data, dcat=False)
#     # Assert
#     assert average == 25


# def test_exclude_dcat_from_report():
#     pass
