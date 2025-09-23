from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override


@dataclass(frozen=True, slots=True)
class Seat(ABC):
    _number: int

    @property
    def number(self) -> int:
        return self._number

    @override
    def __str__(self) -> str:
        return f"<< {self._number} >>"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    @abstractmethod
    def next(self) -> "Seat": ...

    @abstractmethod
    def prev(self) -> "Seat": ...

    @classmethod
    def from_int(cls, number: int):
        return cls(_number=number)
