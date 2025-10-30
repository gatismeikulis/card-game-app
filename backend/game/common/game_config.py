from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True)
class GameConfig(ABC):
    """Game-level configuration.

    This configuration does affect the rules of the game and output of game engine.
    For example, decks to use is a game-level configuration - if it's set, the game engine will use the specified number of decks.
    Another example is the number of cards to deal to each player - if it's set, the game engine will deal the specified number of cards to each player.
    Another example is starting points/chips of the game. Or min bid.
    """

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...
