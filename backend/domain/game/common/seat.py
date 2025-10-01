from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

type SeatNumber = int


@dataclass(frozen=True, slots=True)
class Seat(ABC):
    number: SeatNumber

    @override
    def __str__(self) -> str:
        return f"-{self.number}-"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    @abstractmethod
    def next(self) -> "Seat": ...

    @abstractmethod
    def prev(self) -> "Seat": ...
