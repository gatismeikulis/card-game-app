from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, override

type SeatNumber = int


@dataclass(frozen=True, slots=True)
class Seat(ABC):
    number: SeatNumber

    @abstractmethod
    def next(self) -> Self: ...

    @abstractmethod
    def prev(self) -> Self: ...

    def to_dict(self) -> int:
        """Serialize to seat number"""
        return self.number

    @classmethod
    def from_dict(cls, data: int) -> Self:
        """Reconstruct from seat number"""
        return cls(data)

    @override
    def __str__(self) -> str:
        return f"-{self.number}-"

    @override
    def __repr__(self) -> str:
        return self.__str__()
