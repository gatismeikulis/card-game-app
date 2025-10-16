from typing import Any, Protocol

from .game_config import GameConfig


class GameConfigParser(Protocol):
    def from_dict(self, raw_config: dict[str, Any]) -> GameConfig: ...
