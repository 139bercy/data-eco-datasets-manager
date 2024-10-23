class HTTPError(Exception):
    pass


class DatabaseDeletionError(Exception):
    pass


class ExistingRecordError(Exception):
    pass


class DatasetInconsistencyError(Exception):
    message = "Dataset ID should be the same"
