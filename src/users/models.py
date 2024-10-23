from core.models import get_key


class User:
    def __init__(
        self,
        buid: str,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        permissions: list = None,
        groups: list = None,
        is_active: bool = True,
        joined_at: str = None,
        last_seen_at: str = None,
        last_login_at: str = None
    ):
        self.buid = buid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.permissions = permissions if permissions is not None else []
        self.groups = groups if groups is not None else []
        self.is_active = is_active
        self.joined_at = joined_at
        self.last_seen_at = last_seen_at
        self.last_login_at = last_login_at

    @classmethod
    def create(cls, *args, **kwargs):
        kwargs["buid"] = get_key(f"{kwargs['joined_at']}{kwargs['username']}")
        return cls(**kwargs)

    def update(
        self,
        permissions: list = None,
        groups: list = None,
        is_active: bool = None,
        last_seen_at: str = None,
        last_login_at: str = None
    ):
        if permissions is not None:
            self.permissions = permissions
        if groups is not None:
            self.groups = groups
        if is_active is not None:
            self.is_active = is_active
        if last_seen_at is not None:
            self.last_seen_at = last_seen_at
        if last_login_at is not None:
            self.last_login_at = last_login_at

    def __str__(self):
        return f"<User: {self.username}>"

    def __repr__(self):
        return f"<User: {self.__dict__}>"
