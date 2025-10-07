from collections.abc import Sequence

from backend.domain.core.user import Role, User, UserIdentity
from backend.domain.core.user_id import UserId


class FakeUserRepository:

    def __init__(self):
        self._users: list[User] = [
            User(
                identity=UserIdentity(id=UserId.generate(), username="admin", role=Role.ADMIN),
                name="Admin",
                email="admin@example.com",
                hashed_password="$argon2id$v=19$m=65536,t=3,p=4$+PO8tPk0dczzGxMNDk0fHA$5TAiinbq09VIML1dnA9gi3RptHSRpowPD9mUCFtqMCU",
            ),
        ]

    def find_user_by_username(self, username: str) -> User | None:
        return next((user for user in self._users if user.identity.username == username), None)

    def find_user_by_id(self, id: UserId) -> User | None:
        return next((user for user in self._users if user.identity.id == id), None)

    def create_user(self, user: User) -> User:
        self._users.append(user)
        return user

    def find_users(self) -> Sequence[User]:
        return self._users
