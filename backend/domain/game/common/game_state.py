from abc import ABC
from dataclasses import dataclass

from .seat import Seat


@dataclass(frozen=True, slots=True)
class GameState(ABC):
    active_seat: Seat
