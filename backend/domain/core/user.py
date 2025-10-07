from dataclasses import dataclass
from enum import Enum

from backend.domain.core.user_id import UserId


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    BOT = "bot"


@dataclass(frozen=True, slots=True)
class UserIdentity:
    id: UserId
    username: str
    role: Role


@dataclass(frozen=True, slots=True)
class User:
    identity: UserIdentity
    name: str
    email: str
    hashed_password: str
