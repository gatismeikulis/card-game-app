from collections.abc import Sequence
from typing import final

from backend.application.dtos.user import CreateUserData
from backend.application.interfaces.iuser_repository import IUserRepository
from backend.domain.core.user import Role, User, UserIdentity
from backend.domain.core.user_id import UserId
from pwdlib import PasswordHash


@final
class UserService:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository: IUserRepository = user_repository
        self._password_hash: PasswordHash = PasswordHash.recommended()

    def _hash_password(self, password: str) -> str:
        return self._password_hash.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self._password_hash.verify(password, hashed_password)

    def get_user_by_id(self, id: UserId) -> User | None:
        return self._user_repository.find_user_by_id(id)

    def get_user_by_username(self, username: str) -> User | None:
        return self._user_repository.find_user_by_username(username)

    def create_user(self, user_data: CreateUserData) -> User | None:
        user_id = UserId.generate()
        hashed_password = self._hash_password(user_data.password)
        user = User(
            identity=UserIdentity(
                id=user_id,
                username=user_data.username,
                role=Role.USER,
            ),
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        return self._user_repository.create_user(user)

    def get_users(self) -> Sequence[User]:
        return self._user_repository.find_users()

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.get_user_by_username(username)
        if not user:
            return None
        is_matching_password = self._verify_password(password, user.hashed_password)
        if not is_matching_password:
            return None
        return user
