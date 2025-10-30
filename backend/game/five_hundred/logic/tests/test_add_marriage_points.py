from ....common.seat import Seat
from ..add_marriage_points import add_marriage_points
from ...domain.five_hundred_game import FiveHundredGame


def test_add_marriage_points_logic(sample_game: FiveHundredGame):
    game = add_marriage_points(sample_game, 40, Seat(1))

    assert game.round.seat_infos[Seat(1)].marriage_points == list(
        sample_game.round.seat_infos[Seat(1)].marriage_points
    ) + [40]
    assert game.round.seat_infos[Seat(1)].points == sample_game.round.seat_infos[Seat(1)].points + 40
    assert game.round.is_marriage_announced is True
