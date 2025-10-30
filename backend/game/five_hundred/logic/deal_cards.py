from collections.abc import Mapping
from dataclasses import replace

from ...common.hand import Hand
from ..domain.five_hundred_deck import FiveHundredDeck
from ...common.seat import Seat
from ..domain.five_hundred_phase import FiveHundredPhase
from ..domain.five_hundred_seat_info import FiveHundredSeatInfo
from ..domain.constants import CARDS_IN_STARTING_HAND, CARDS_TO_TAKE
from ..domain.five_hundred_game import FiveHundredGame


def deal_cards(game: FiveHundredGame, deck: FiveHundredDeck) -> FiveHundredGame:
    cards_to_take = deck.draw_many(CARDS_TO_TAKE)

    seat_infos_updated: Mapping[Seat, FiveHundredSeatInfo] = {
        seat: replace(seat_info, hand=Hand(tuple(deck.draw_many(CARDS_IN_STARTING_HAND))))
        for seat, seat_info in game.round.seat_infos.items()
    }

    round_updated = replace(
        game.round, seat_infos=seat_infos_updated, cards_to_take=cards_to_take, phase=FiveHundredPhase.BIDDING
    )

    return replace(game, round=round_updated)
