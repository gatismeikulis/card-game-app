from abc import ABC
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class GameEvent(ABC):
    type: ClassVar[str]  # event kind/type
