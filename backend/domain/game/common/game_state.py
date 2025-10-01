from abc import ABC, abstractmethod
from dataclasses import dataclass

from .seat import Seat


@dataclass(frozen=True, slots=True)
class GameState(ABC):
    active_seat: Seat

    @abstractmethod
    def str_repr_for_table(self) -> str: ...
