from typing import Any, Protocol

from .game_command import GameCommand


class GameCommandParser(Protocol):
    def from_dict(self, raw_command: dict[str, Any]) -> GameCommand: ...
