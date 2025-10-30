from collections.abc import Sequence
from typing import override

from ..common.seat import SeatNumber
from ..common.game_config import GameConfig
from ..common.game_exception import GameEngineException
from ..common.game_engine import GameEngine
from ..common.game_command import GameCommand
from ..common.game_event import GameEvent
from ..common.game_state import GameState
from .application.apply_event import apply_event
from .application.process_command import process_command
from .domain.five_hundred_command import FiveHundredCommand, StartGameCommand
from .domain.five_hundred_game_config import FiveHundredGameConfig
from .domain.five_hundred_event import FiveHundredEvent
from .domain.five_hundred_game import FiveHundredGame


class FiveHundredGameEngine(GameEngine):
    @override
    def process_command(self, game_state: GameState, command: GameCommand) -> tuple[GameState, Sequence[GameEvent]]:
        # Validate and narrow types to Five Hundred specifics
        if not isinstance(game_state, FiveHundredGame):
            raise GameEngineException(
                detail=f"Could not process command: expected FiveHundredGame, got {type(game_state).__name__}"
            )
        if not isinstance(command, FiveHundredCommand):
            raise GameEngineException(
                detail=f"Could not process command: expected FiveHundredCommand, got {type(command).__name__}"
            )
        game_state_updated, events = process_command(game_state, command)
        return game_state_updated, events

    @override
    def start_game(
        self, game_config: GameConfig, taken_seat_numbers: frozenset[SeatNumber]
    ) -> tuple[GameState, Sequence[GameEvent]]:
        if not isinstance(game_config, FiveHundredGameConfig):
            raise GameEngineException(
                detail=f"Could not start the game: expected FiveHundredGameConfig, got {type(game_config).__name__}"
            )
        game_state = FiveHundredGame.init(game_config, taken_seat_numbers)
        command = StartGameCommand()
        game_state_updated, events = process_command(game_state, command)
        return game_state_updated, events

    @override
    def restore_game_state(
        self, events: Sequence[GameEvent], game_config: GameConfig, taken_seat_numbers: frozenset[SeatNumber]
    ) -> GameState:
        if not isinstance(game_config, FiveHundredGameConfig):
            raise GameEngineException(
                detail=f"Could not initialize the game state: expected FiveHundredGameConfig, got {type(game_config).__name__}"
            )
        restored_game_state = FiveHundredGame.init(game_config, taken_seat_numbers)
        for event in events:
            # Validate and narrow event type to Five Hundred specifics
            if not isinstance(event, FiveHundredEvent):
                raise GameEngineException(
                    detail=f"Could not restore game state: expected FiveHundredEvent, got {type(event).__name__}"
                )
            print(event)
            restored_game_state = apply_event(restored_game_state, event)

        return restored_game_state
