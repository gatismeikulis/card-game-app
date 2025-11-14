from collections.abc import Mapping
from dataclasses import replace

from ...common.seat import Seat
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_round import FiveHundredRound


def finish_round(game: FiveHundredGame, points_per_seat: Mapping[Seat, int]) -> FiveHundredGame:
    game_summary_updated = {seat: game.summary[seat] + points_per_seat[seat] for seat in points_per_seat.keys()}

    first_seat_updated = game.round.first_seat.next(game.taken_seats)

    round_updated = FiveHundredRound.create(game.round.round_number + 1, first_seat_updated, game.taken_seats)

    # round ended, we can allow to create replay views up to this point
    replay_safe_event_number_updated = game.event_number

    return replace(
        game,
        active_seat=first_seat_updated,
        summary=game_summary_updated,
        round=round_updated,
        replay_safe_event_number=replay_safe_event_number_updated,
    )
