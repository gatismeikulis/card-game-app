import random

from ..domain.constants import BID_STEP, MAX_BID, MIN_BID, NOT_ALLOWED_TO_BID_THRESHOLD
from ..domain.five_hundred_command import FiveHundredCommand, MakeBidCommand, PassCardsCommand, PlayCardCommand
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


def create_automatic_command(game: FiveHundredGame) -> FiveHundredCommand:
    match game.round.phase:
        case FiveHundredPhase.BIDDING:
            highest_bid = game.round.highest_bid[1] if game.round.highest_bid else MIN_BID
            passing_probability = highest_bid / MAX_BID + 0.2

            if game.summary[game.active_seat] >= NOT_ALLOWED_TO_BID_THRESHOLD:
                return MakeBidCommand(bid=-1)
            if random.random() < passing_probability:
                return MakeBidCommand(bid=-1)
            return MakeBidCommand(bid=random.choice(range(highest_bid, MAX_BID + 1, BID_STEP)))

        case FiveHundredPhase.FORMING_HANDS:
            active_seats_cards = list(game.active_seats_info.hand.cards)
            card1, card2 = random.sample(active_seats_cards, 2)

            return PassCardsCommand(card_to_next_seat=card1, card_to_prev_seat=card2)

        case FiveHundredPhase.PLAYING_CARDS:
            cards_allowed_to_play = game.active_seats_info.cards_allowed_to_play(
                game.round.required_suit, game.round.trump_suit
            )

            card_to_play = random.choice(cards_allowed_to_play)
            return PlayCardCommand(card=card_to_play)

        case _:
            raise ValueError(f"Invalid phase: {game.round.phase}")
