from collections.abc import Sequence

from ..common.game_command import GameCommand
from ..common.game_event import GameEvent
from ..common.game_state import GameState
from .application.process_command import process_command
from .domain.five_hundred_command import FiveHundredCommand, StartGameCommand
from .domain.five_hundred_game import FiveHundredGame
from .domain.five_hundred_round import FiveHundredRound
from .domain.five_hundred_seat import FiveHundredSeat


class FiveHundredGameEngine:
    def process_command(self, game_state: GameState, command: GameCommand) -> tuple[GameState, Sequence[GameEvent]]:
        # Validate and narrow types to Five Hundred specifics
        if not isinstance(game_state, FiveHundredGame):
            raise TypeError(f"FiveHundredGameEngine expects FiveHundredGame, got {type(game_state).__name__}")
        if not isinstance(command, FiveHundredCommand):
            raise TypeError(f"FiveHundredGameEngine expects FiveHundredCommand, got {type(command).__name__}")
        game_state_updated, events = process_command(game_state, command)
        return game_state_updated, events

    def init_game(self) -> tuple[GameState, Sequence[GameEvent]]:
        round = FiveHundredRound.create(1, FiveHundredSeat(1))
        game_state = FiveHundredGame.create(round)
        command = StartGameCommand()
        game_state_updated, events = process_command(game_state, command)
        return game_state_updated, events
