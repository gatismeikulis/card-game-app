from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TableConfig(ABC):
    automatic_start: bool  # true - start game automatically without asking players to agree to start

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...
