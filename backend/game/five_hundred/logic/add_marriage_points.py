from dataclasses import replace

from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_seat import FiveHundredSeat


def add_marriage_points(game: FiveHundredGame, points: int, add_to: FiveHundredSeat) -> FiveHundredGame:
    seat_info = game.round.seat_infos[add_to]

    marriage_points_updated = list(seat_info.marriage_points) + [points]

    seat_info_updated = replace(
        seat_info,
        marriage_points=marriage_points_updated,
        points=seat_info.points + points,
    )

    seat_infos_updated = dict(game.round.seat_infos) | {add_to: seat_info_updated}

    round_updated = replace(game.round, seat_infos=seat_infos_updated, is_marriage_announced=True)

    return replace(game, round=round_updated)
