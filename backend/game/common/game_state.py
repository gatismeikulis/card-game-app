from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .seat import Seat, SeatNumber


@dataclass(frozen=True, slots=True)
class GameState(ABC):
    active_seat: Seat
    is_finished: bool

    @abstractmethod
    def str_repr_for_table(self) -> str: ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "GameState": ...

    @abstractmethod
    def to_public_dict(self, seat_number: SeatNumber | None = None) -> dict[str, Any]: ...
