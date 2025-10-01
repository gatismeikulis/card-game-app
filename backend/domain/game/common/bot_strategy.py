from typing import Protocol

from .game_command import GameCommand
from .game_state import GameState


class BotStrategy(Protocol):
    def create_command(self, game_state: GameState) -> GameCommand: ...
