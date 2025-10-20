from collections.abc import Mapping
from dataclasses import replace


from ...common.hand import Hand
from ..domain.five_hundred_deck import FiveHundredDeck
from ..domain.five_hundred_seat import FiveHundredSeat
from ..domain.five_hundred_seat_info import FiveHundredSeatInfo
from ..domain.constants import CARDS_IN_STARTING_HAND, CARDS_TO_TAKE
from ..domain.five_hundred_game import FiveHundredGame


def deal_cards(game: FiveHundredGame, deck: FiveHundredDeck) -> FiveHundredGame:
    cards_to_take = deck.draw_many(CARDS_TO_TAKE)
    seat_one_cards = deck.draw_many(CARDS_IN_STARTING_HAND)
    seat_two_cards = deck.draw_many(CARDS_IN_STARTING_HAND)
    seat_three_cards = deck.draw_many(CARDS_IN_STARTING_HAND)

    seat_one_hand = Hand(tuple(seat_one_cards))
    seat_two_hand = Hand(tuple(seat_two_cards))
    seat_three_hand = Hand(tuple(seat_three_cards))

    seat_one_updated = replace(game.round.seat_infos[FiveHundredSeat(1)], hand=seat_one_hand)
    seat_two_updated = replace(game.round.seat_infos[FiveHundredSeat(2)], hand=seat_two_hand)
    seat_three_updated = replace(game.round.seat_infos[FiveHundredSeat(3)], hand=seat_three_hand)

    seat_infos_updated: Mapping[FiveHundredSeat, FiveHundredSeatInfo] = {
        FiveHundredSeat(1): seat_one_updated,
        FiveHundredSeat(2): seat_two_updated,
        FiveHundredSeat(3): seat_three_updated,
    }

    round_updated = replace(game.round, seat_infos=seat_infos_updated, cards_to_take=cards_to_take)

    return replace(game, round=round_updated)
