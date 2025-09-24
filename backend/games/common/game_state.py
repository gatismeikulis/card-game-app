from abc import ABC, abstractmethod
from dataclasses import dataclass

from .seat import Seat


@dataclass(frozen=True, slots=True)
class GameState(ABC):

    @property
    @abstractmethod
    def active_seat(self) -> Seat: ...
