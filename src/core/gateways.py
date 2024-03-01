import abc


class AbstractDatasetRepository(abc.ABC):   # pragma: no cover
    @abc.abstractmethod
    def get_all(self):
        pass

    @abc.abstractmethod
    def get_one(self, dataset_id: str):
        pass
