from tinydb import TinyDB, Query

from infrastructure.builder import TinyDBQueryBuilder
from infrastructure.exceptions import ExistingRecordError
from users.models import User


class InMemoryUsersRepository:
    def __init__(self, db: list):
        self.db = db

    def get_all(self):
        raise NotImplementedError

    def get_one(self, username: str):
        user = next((user for user in self.db if user.username == username), None)
        return user

    def add(self, user: User):
        if self.is_unique(username=user.username):
            self.db.append(user)
        else:
            raise ExistingRecordError

    def update(self, username: str, values: dict):
        user = next((user for user in self.db if user.username == username), None)
        if user:
            [setattr(user, key, value) for key, value in values.items()]
            return user
        else:
            raise ValueError("Dataset with ID {} not found".format(username))

    def upsert(self, user):
        try:
            self.add(user)
        except ExistingRecordError:
            self.update(user.username, user.__dict__)

    def is_unique(self, username):
        index = {value.username for value in self.db}
        result = next((user for user in index if username == username), None)
        if result:
            return False
        return True


class TinyDbUserRepository:
    def __init__(self, name):
        self.name = name
        self.db = TinyDB(name, indent=2, ensure_ascii=False)
        self.builder = TinyDBQueryBuilder(db=self.db)
        self.users = self.db.table('users')

    def all(self):
        return self.users.all()

    def one(self, username: str):
        query = Query()
        result = self.users.search(query.username == username)[0]
        dataset = User(**result)
        return dataset

    def is_unique(self, username):
        index = {value["username"] for value in self.users.all()}
        result = next((dsid for dsid in index if dsid == username), None)
        if result:
            return False
        return True

    def add(self, user: User):
        if self.is_unique(username=user.username):
            self.users.insert(user.__dict__)
        else:
            raise ExistingRecordError

    def upsert(self, user: User):
        try:
            self.add(user=user)
        except ExistingRecordError:
            self.update(user.username, user.__dict__)

    def update(self, username: str, values: dict) -> None:
        query = Query()
        self.users.update(values, query.username == username)
