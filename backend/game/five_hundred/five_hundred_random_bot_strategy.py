import random
from typing import override

from ..common.game_exception import GameEngineException
from ..bot_strategy_kind import BotStrategyKind
from ..common.bot_strategy import BotStrategy
from ..common.game_command import GameCommand
from ..common.game_state import GameState
from .domain.constants import BID_STEP, MAX_BID, MIN_BID, NOT_ALLOWED_TO_BID_THRESHOLD
from .domain.five_hundred_command import (
    MakeBidCommand,
    PassCardsCommand,
    PlayCardCommand,
)
from .domain.five_hundred_game import FiveHundredGame
from .domain.five_hundred_phase import FiveHundredPhase


class FiveHundredRandomBotStrategy(BotStrategy):
    kind: BotStrategyKind = BotStrategyKind.RANDOM

    @override
    def create_command(self, game_state: GameState) -> GameCommand:
        if not isinstance(game_state, FiveHundredGame):
            raise GameEngineException(
                detail=f"Could not create bot strategy command: expected FiveHundredGame, got {type(game_state).__name__}"
            )
        match game_state.round.phase:
            case FiveHundredPhase.BIDDING:
                highest_bid = game_state.round.highest_bid[1] if game_state.round.highest_bid else MIN_BID
                passing_probability = highest_bid / MAX_BID + 0.3

                if game_state.summary[game_state.active_seat] >= NOT_ALLOWED_TO_BID_THRESHOLD:
                    return MakeBidCommand(bid=-1)
                if random.random() < passing_probability:
                    return MakeBidCommand(bid=-1)
                return MakeBidCommand(bid=random.choice(range(highest_bid, MAX_BID + 1, BID_STEP)))

            case FiveHundredPhase.FORMING_HANDS:
                active_seats_cards = list(game_state.active_seats_info.hand.cards)
                card1, card2 = random.sample(active_seats_cards, 2)

                return PassCardsCommand(card_to_next_seat=card1, card_to_prev_seat=card2)

            case FiveHundredPhase.PLAYING_CARDS:
                cards_allowed_to_play = game_state.active_seats_info.cards_allowed_to_play(
                    game_state.round.required_suit, game_state.round.trump_suit
                )

                card_to_play = random.choice(cards_allowed_to_play)
                return PlayCardCommand(card=card_to_play)

            case _:
                raise GameEngineException(
                    detail=f"Could not create bot strategy command: invalid phase: {game_state.round.phase}"
                )
