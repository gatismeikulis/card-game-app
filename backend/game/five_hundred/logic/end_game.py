from collections.abc import Sequence
from dataclasses import replace

from ...common.seat import Seat
from ...common.game_ending import GameEnding, GameEndingReason
from ..domain.constants import GAME_STARTING_POINTS
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


def end_game(game: FiveHundredGame, reason: GameEndingReason, blamed_seat: Seat | None) -> FiveHundredGame:
    round_updated = replace(
        game.round,
        phase=FiveHundredPhase.GAME_ENEDED,
        seat_infos={},
        cards_on_board={},
        cards_to_take=[],
        required_suit=None,
        trump_suit=None,
        highest_bid=None,
        round_number=0,
        is_marriage_announced=False,
    )

    winners: Sequence[Seat] = []
    losers: Sequence[Seat] = []
    point_differences = {seat: GAME_STARTING_POINTS - points for seat, points in game.summary.items()}

    match reason:
        case GameEndingReason.FINISHED:
            if game.round.round_number >= game.game_config.max_rounds:
                winners = [
                    seat for seat, points in game.summary.items() if points == min(game.summary.values())
                ]  # seats with lowest points are the winners
            else:
                winners = [seat for seat, points in game.summary.items() if points <= 0]
            losers = [seat for seat in game.taken_seats if seat not in winners]
        case GameEndingReason.ABORTED:
            losers = [blamed_seat] if blamed_seat else []
            winners = [seat for seat in game.taken_seats if seat != blamed_seat]
        case GameEndingReason.CANCELLED:
            pass  # default values are already set

    return replace(
        game,
        round=round_updated,
        ending=GameEnding(winners=winners, losers=losers, reason=reason, point_differences=point_differences),
        replay_safe_event_number=game.event_number,
    )
