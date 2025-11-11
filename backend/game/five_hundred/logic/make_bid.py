from dataclasses import replace

from ..domain.five_hundred_game import FiveHundredGame
from .helpers import get_next_seat_to_bid


def make_bid(game: FiveHundredGame, bid: int) -> FiveHundredGame:
    active_seat = game.active_seat

    highest_bid_updated = (active_seat, bid) if (bid > 0) else game.round.highest_bid

    active_seats_info_updated = replace(game.round.seat_infos[active_seat], bid=bid)

    seat_infos_updated = dict(game.round.seat_infos) | {active_seat: active_seats_info_updated}

    round_updated = replace(
        game.round,
        seat_infos=seat_infos_updated,
        highest_bid=highest_bid_updated,
    )

    next_seat_to_bid = get_next_seat_to_bid(active_seat, game.round.seat_infos)

    turn_number_updated = game.turn_number + 1

    return replace(
        game,
        round=round_updated,
        active_seat=(next_seat_to_bid if next_seat_to_bid is not None else active_seat),
        turn_number=turn_number_updated,
    )
