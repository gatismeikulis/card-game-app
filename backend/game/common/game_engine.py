from collections.abc import Sequence
from typing import Protocol

from .seat import SeatNumber
from .game_config import GameConfig
from .game_command import GameCommand
from .game_event import GameEvent
from .game_state import GameState


class GameEngine(Protocol):
    def start_game(
        self, game_config: GameConfig, taken_seat_numbers: frozenset[SeatNumber]
    ) -> tuple[GameState, Sequence[GameEvent]]: ...

    def process_command(self, game_state: GameState, command: GameCommand) -> tuple[GameState, Sequence[GameEvent]]: ...

    def apply_event(self, game_state: GameState, event: GameEvent) -> GameState: ...

    def init_game_state(self, game_config: GameConfig, taken_seat_numbers: frozenset[SeatNumber]) -> GameState: ...
