from dataclasses import replace
import pytest

from ...domain.five_hundred_round_results import FiveHundredRoundResults
from ..finish_round import finish_round
from ...domain.five_hundred_game import FiveHundredGame


@pytest.mark.parametrize(
    "points_per_seat_number,expected_results_per_seat_number, expected_summary_per_seat_number",
    # assuming highest bidder was seat 1 with bid 100 and all seats are at STARTING_POINTS
    [
        (
            {1: 47, 2: 9, 3: 64},
            {1: 100, 2: -10, 3: -65},
            {1: 600, 2: 490, 3: 435},
        ),  # highest bidder failed to exceed the bid
        ({1: 103, 2: 17, 3: 0}, {1: -100, 2: -15, 3: 0}, {1: 400, 2: 485, 3: 500}),  # highest bidder exceeded the bid
    ],
    ids=[
        "highest_bidder_failed_to_exceed_the_bid",
        "highest_bidder_exceeded_the_bid",
    ],
)
def test_finish_round_scoring_logic(
    sample_game: FiveHundredGame,
    points_per_seat_number: dict[int, int],
    expected_results_per_seat_number: dict[int, int],
    expected_summary_per_seat_number: dict[int, int],
):
    sample_round = sample_game.round
    sample_seat_infos = sample_game.round.seat_infos
    sample_seat_infos_updated = {
        seat: replace(seat_info, points=points_per_seat_number[seat.number])
        for seat, seat_info in sample_seat_infos.items()
    }
    sample_round_updated = replace(sample_round, seat_infos=sample_seat_infos_updated)
    sample_game_updated = replace(sample_game, round=sample_round_updated)
    game = finish_round(sample_game_updated)

    expected_round_result = FiveHundredRoundResults(
        round_number=sample_game.round.round_number,
        bidding_results=sample_round.highest_bid,
        seat_points={seat: expected_results_per_seat_number[seat.number] for seat in sample_seat_infos.keys()},
    )

    assert game.results[-1] == expected_round_result
    assert game.summary == {seat: expected_summary_per_seat_number[seat.number] for seat in sample_seat_infos.keys()}
