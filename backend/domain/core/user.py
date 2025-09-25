from dataclasses import dataclass

from backend.domain.core.user_id import UserId


@dataclass(frozen=True, slots=True)
class User:
    id: UserId
    name: str
