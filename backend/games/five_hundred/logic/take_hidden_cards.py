from dataclasses import replace

from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_game import FiveHundredGame


def take_hidden_cards(game: FiveHundredGame) -> FiveHundredGame:
    active_seat = game.active_seat
    active_seats_info = game.active_seats_info

    active_seats_hand_updated = active_seats_info.hand.with_added_cards(game.round.cards_to_take)

    active_seats_info_updated = replace(active_seats_info, hand=active_seats_hand_updated)

    seat_infos_updated = dict(game.round.seat_infos) | {active_seat: active_seats_info_updated}

    cards_to_take_updated: list[FiveHundredCard] = []

    round_updated = replace(
        game.round,
        seat_infos=seat_infos_updated,
        cards_to_take=cards_to_take_updated,
    )

    return replace(game, round=round_updated)
