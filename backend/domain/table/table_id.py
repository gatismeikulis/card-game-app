from dataclasses import dataclass
from typing import override
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class TableId:
    value: UUID

    @staticmethod
    def from_str(value: str) -> "TableId":
        return TableId(UUID(value))

    @staticmethod
    def generate() -> "TableId":
        return TableId(uuid4())

    @override
    def __str__(self) -> str:
        return "table-id-" + str(self.value)

    @override
    def __repr__(self) -> str:
        return self.__str__()
