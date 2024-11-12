from users.api import user_dto
from users.models import User


def import_user(repository, user: dict):
    dto = user_dto(user=user)
    user = User.create(**dto)
    repository.upsert(user=user)
    return user
