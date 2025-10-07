from collections.abc import Sequence
from typing import Protocol

from backend.domain.core.user import User
from backend.domain.core.user_id import UserId


class IUserRepository(Protocol):

    # in concrete implementation, include methods like _to_entity, _to_model

    def find_user_by_username(self, username: str) -> User | None: ...

    def find_user_by_id(self, id: UserId) -> User | None: ...

    def create_user(self, user: User) -> User: ...

    def find_users(self) -> Sequence[User]: ...
