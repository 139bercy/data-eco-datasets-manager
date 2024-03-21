import abc


class AbstractDatasetRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_one(self, dataset_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, dataset):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, dataset_id: str, values: dict) -> None:
        raise NotImplementedError
