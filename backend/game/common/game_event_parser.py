from typing import Any, Protocol

from .game_event import GameEvent


class GameEventParser(Protocol):
    def from_dict(self, data: dict[str, Any]) -> GameEvent: ...
