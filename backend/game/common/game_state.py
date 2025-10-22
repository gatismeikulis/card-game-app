from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self

from .seat import Seat, SeatNumber


@dataclass(frozen=True, slots=True)
class GameState(ABC):
    active_seat: Seat
    is_finished: bool

    @classmethod
    @abstractmethod
    def init(cls) -> Self: ...

    @abstractmethod
    def str_repr_for_table(self) -> str: ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...

    @abstractmethod
    def to_public_dict(self, seat_number: SeatNumber | None = None) -> dict[str, Any]: ...
