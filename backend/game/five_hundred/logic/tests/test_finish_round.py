from dataclasses import replace
import pytest

from ..finish_round import finish_round
from ...domain.five_hundred_game import FiveHundredGame
from ....common.seat import Seat


@pytest.mark.parametrize(
    "points_per_seat_number, expected_summary_per_seat_number",
    # assuming all seats are at STARTING_POINTS
    [
        (
            {1: 100, 2: -50, 3: -60},
            {1: 600, 2: 450, 3: 440},
        ),
        (
            {1: 0, 2: 0, 3: 0},
            {1: 500, 2: 500, 3: 500},
        ),
    ],
    ids=[
        "point_updates_for_all_seats",
        "no_point_updates",
    ],
)
def test_finish_round_logic(
    sample_game: FiveHundredGame,
    points_per_seat_number: dict[int, int],
    expected_summary_per_seat_number: dict[int, int],
):
    sample_game_updated = replace(sample_game, event_number=15)
    points_per_seat = {Seat(seat_number): points for seat_number, points in points_per_seat_number.items()}
    game = finish_round(sample_game_updated, points_per_seat)

    assert game.summary == {seat: expected_summary_per_seat_number[seat.number] for seat in game.taken_seats}
    assert game.replay_safe_event_number == sample_game_updated.event_number
