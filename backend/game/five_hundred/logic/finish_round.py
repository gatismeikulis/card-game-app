from dataclasses import replace

from ...common.seat import Seat
from ..domain.constants import MUST_BID_THRESHOLD
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_round import FiveHundredRound
from ..domain.five_hundred_round_results import FiveHundredRoundResults


def finish_round(game: FiveHundredGame) -> FiveHundredGame:
    bidding_winning_seat = game.round.highest_bid[0] if game.round.highest_bid else None

    def get_round_points_for_seat(seat: Seat, seats_game_points: int) -> int:
        points = game.round.seat_infos[seat].points
        if bidding_winning_seat == seat:
            winning_bid = game.round.highest_bid[1] if game.round.highest_bid else 0
            return winning_bid if winning_bid <= points else -winning_bid
        else:
            diff_of_five = points % 5
            points_rounded = points - diff_of_five + 5 if diff_of_five > 2 else points - diff_of_five
            return points_rounded if seats_game_points >= MUST_BID_THRESHOLD else 0

    seat_points = {seat: -get_round_points_for_seat(seat, game.summary[seat]) for seat in game.round.seat_infos.keys()}

    round_results = FiveHundredRoundResults(
        round_number=game.round.round_number,
        bidding_results=game.round.highest_bid,
        seat_points=seat_points,
    )

    game_summary_updated = {seat: game.summary[seat] + seat_points[seat] for seat in seat_points.keys()}

    first_seat_updated = game.round.first_seat.next(game.taken_seats)

    round_updated = FiveHundredRound.create(game.round.round_number + 1, first_seat_updated, game.taken_seats)

    return replace(
        game,
        active_seat=first_seat_updated,
        results=list(game.results) + [round_results],
        summary=game_summary_updated,
        round=round_updated,
    )
