from dataclasses import dataclass
from typing import override
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID

    @staticmethod
    def from_str(value: str) -> "UserId":
        return UserId(UUID(value))

    @staticmethod
    def generate() -> "UserId":
        return UserId(uuid4())

    @override
    def __str__(self) -> str:
        return "user-id-" + str(self.value)

    @override
    def __repr__(self) -> str:
        return self.__str__()
