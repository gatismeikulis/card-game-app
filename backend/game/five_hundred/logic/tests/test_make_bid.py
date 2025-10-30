from ..helpers import get_next_seat_to_bid
from ....common.seat import Seat
from ..make_bid import make_bid
from ...domain.five_hundred_game import FiveHundredGame


def test_make_bid_with_non_passing_bid(sample_game: FiveHundredGame):
    bid = 120
    game = make_bid(sample_game, bid=bid)

    bid_making_seat = sample_game.active_seat
    assert game.round.seat_infos[bid_making_seat].bid == bid
    assert game.round.highest_bid == (bid_making_seat, bid)
    assert game.active_seat == get_next_seat_to_bid(bid_making_seat, game.round.seat_infos)


def test_make_bid_with_passing_bid(sample_game: FiveHundredGame):
    game = make_bid(sample_game, bid=-5)

    bid_making_seat = sample_game.active_seat
    assert game.round.seat_infos[bid_making_seat].bid == -5
    assert game.round.highest_bid == sample_game.round.highest_bid
    assert game.active_seat == Seat(2)
