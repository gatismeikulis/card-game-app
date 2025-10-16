from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GameConfig(ABC):
    min_seats: int
    max_seats: int

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...
