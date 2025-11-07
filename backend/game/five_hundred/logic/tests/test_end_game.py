from dataclasses import replace
import pytest

from ....common.game_ending import GameEnding, GameEndingReason
from ....common.seat import Seat
from ...domain.five_hundred_phase import FiveHundredPhase
from ...domain.five_hundred_game import FiveHundredGame
from ..end_game import end_game


@pytest.mark.parametrize(
    "game_points_per_seat_number, ending_reason, blamed_seat, round_number, expected_game_ending",
    # assuming max rounds is 100 and taken_seats is {1, 2, 3}
    [
        (
            {1: 600, 2: 80, 3: 80},
            GameEndingReason.FINISHED,
            None,
            100,
            GameEnding(
                winners=[Seat(2), Seat(3)],
                losers=[Seat(1)],
                reason=GameEndingReason.FINISHED,
                point_differences={Seat(1): -100, Seat(2): 420, Seat(3): 420},
            ),
        ),
        (
            {1: 0, 2: 700, 3: 95},
            GameEndingReason.FINISHED,
            None,
            50,
            GameEnding(
                winners=[Seat(1)],
                losers=[Seat(2), Seat(3)],
                reason=GameEndingReason.FINISHED,
                point_differences={Seat(1): 500, Seat(2): -200, Seat(3): 405},
            ),
        ),
        (
            {1: 300, 2: 0, 3: 0},
            GameEndingReason.FINISHED,
            None,
            50,
            GameEnding(
                winners=[Seat(2), Seat(3)],
                losers=[Seat(number=1)],
                reason=GameEndingReason.FINISHED,
                point_differences={Seat(1): 200, Seat(2): 500, Seat(3): 500},
            ),
        ),
        (
            {1: 1050, 2: 1020, 3: 1100},
            GameEndingReason.FINISHED,
            None,
            20,
            GameEnding(
                winners=[],
                losers=[Seat(number=1), Seat(number=2), Seat(3)],
                reason=GameEndingReason.FINISHED,
                point_differences={Seat(1): -550, Seat(2): -520, Seat(3): -600},
            ),
        ),
        (
            {1: 300, 2: 400, 3: 700},
            GameEndingReason.ABORTED,
            Seat(number=2),
            20,
            GameEnding(
                winners=[Seat(number=1), Seat(3)],
                losers=[Seat(number=2)],
                reason=GameEndingReason.ABORTED,
                point_differences={Seat(1): 200, Seat(2): 100, Seat(3): -200},
            ),
        ),
        (
            {1: 600, 2: 300, 3: 300},
            GameEndingReason.CANCELLED,
            None,
            50,
            GameEnding(
                winners=[],
                losers=[],
                reason=GameEndingReason.CANCELLED,
                point_differences={Seat(1): -100, Seat(2): 200, Seat(3): 200},
            ),
        ),
    ],
    ids=[
        "finished_by_reaching_max_rounds",
        "finished_by_player_reaching_0_points",
        "finished_by_multiple_players_reaching_0_points",
        "finished_by_all_players_reaching_allowed_to_bid_threshold",
        "finished_by_aborted",
        "finished_by_cancelled",
    ],
)
def test_end_game_logic(
    sample_game: FiveHundredGame,
    game_points_per_seat_number: dict[int, int],
    ending_reason: GameEndingReason,
    blamed_seat: Seat | None,
    round_number: int,
    expected_game_ending: GameEnding,
):
    sample_round = sample_game.round
    sample_round_updated = replace(sample_round, round_number=round_number)
    summary_updated = {Seat(seat_number): points for seat_number, points in game_points_per_seat_number.items()}
    sample_game_updated = replace(sample_game, round=sample_round_updated, summary=summary_updated)
    game = end_game(sample_game_updated, ending_reason, blamed_seat)

    assert game.ending == expected_game_ending
    assert game.round.phase == FiveHundredPhase.GAME_ENEDED
