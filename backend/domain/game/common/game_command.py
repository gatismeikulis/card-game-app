from abc import ABC
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class GameCommand(ABC):
    type: ClassVar[str]  # command kind/type
