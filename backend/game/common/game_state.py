from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self

from .game_config import GameConfig
from .seat import Seat, SeatNumber


@dataclass(frozen=True, slots=True)
class GameState(ABC):
    active_seat: Seat
    is_ended: bool
    game_config: GameConfig
    taken_seats: frozenset[Seat]

    @classmethod
    @abstractmethod
    def init(cls, game_config: GameConfig, taken_seat_numbers: frozenset[SeatNumber]) -> Self: ...

    @abstractmethod
    def str_repr_for_table(self) -> str: ...

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...

    @abstractmethod
    def to_public_dict(self, seat_number: SeatNumber | None = None) -> dict[str, Any]: ...
