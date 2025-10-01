from abc import ABC
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class GameEvent(ABC):
    source: ClassVar[str]  # game name
    type: ClassVar[str]  # event kind/type
