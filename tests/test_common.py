from core.configuration import format_filename
from freezegun import freeze_time


@freeze_time("2024-01-01")
def test_format_filename_with_directory():
    # Act
    path = format_filename(filename="datasets.json", directory="data")
    # Assert
    assert path == "data/2024-01-01-datasets.json"


@freeze_time("2024-01-01")
def test_format_filename():
    # Act
    path = format_filename(filename="datasets.json", directory=".")
    # Assert
    assert path == "./2024-01-01-datasets.json"
