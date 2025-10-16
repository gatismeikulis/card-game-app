from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Any, Self


@dataclass(frozen=True, slots=True)
class GameEvent(ABC):
    type: ClassVar[str]  # event kind/type

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...
