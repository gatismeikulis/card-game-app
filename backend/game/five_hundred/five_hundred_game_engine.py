from collections.abc import Sequence

from ..common.game_command import GameCommand
from ..common.game_event import GameEvent
from ..common.game_state import GameState
from .application.apply_event import apply_event
from .application.process_command import process_command
from .logic.deal_cards import deal_cards
from .domain.five_hundred_command import FiveHundredCommand
from .domain.five_hundred_event import FiveHundredEvent
from .domain.five_hundred_game import FiveHundredGame
from .domain.five_hundred_deck import FiveHundredDeck
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

    def init_game(self) -> GameState:
        round = FiveHundredRound.create(1, FiveHundredSeat(1))
        game = FiveHundredGame.create(round)
        deck = FiveHundredDeck.build()
        # workaround to get initial game state with cards already dealt.
        # for the next rounds it will happen in normal flow (when event is applied)
        game_with_cards_for_first_round_dealt = deal_cards(game, deck)
        return game_with_cards_for_first_round_dealt

    def rebuild_game_state(self, initial_game_state: GameState, events: Sequence[GameEvent]) -> GameState:
        # Validate and narrow types to Five Hundred specifics
        if not isinstance(initial_game_state, FiveHundredGame):
            raise TypeError(f"FiveHundredGameEngine expects FiveHundredGame, got {type(initial_game_state).__name__}")
        rebuilt_game_state = initial_game_state
        for event in events:
            if not isinstance(event, FiveHundredEvent):
                raise TypeError(f"FiveHundredGameEngine expects FiveHundredEvent, got {type(event).__name__}")
            rebuilt_game_state = apply_event(rebuilt_game_state, event)

        return rebuilt_game_state
