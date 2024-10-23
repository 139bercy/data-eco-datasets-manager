import abc

from users.models import User


class AbstractDatasetRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def one(self, dataset_id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def upsert(self, dataset):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, dataset):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, dataset_id: str, values: dict) -> None:
        raise NotImplementedError


class AbstractUsersRepository(abc.ABC):  # pragma: no cover
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def one(self, username: str):
        raise NotImplementedError

    @abc.abstractmethod
    def upsert(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, username: str):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, username: str, values: dict) -> None:
        raise NotImplementedError
