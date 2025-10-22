from collections.abc import Sequence
from typing import Protocol

from .game_command import GameCommand
from .game_event import GameEvent
from .game_state import GameState


class GameEngine(Protocol):
    def init_game(self) -> tuple[GameState, Sequence[GameEvent]]: ...
    def process_command(self, game_state: GameState, command: GameCommand) -> tuple[GameState, Sequence[GameEvent]]: ...
