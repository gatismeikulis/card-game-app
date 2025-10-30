from dataclasses import replace

from ...common.seat import Seat
from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_game import FiveHundredGame


def take_trick(game: FiveHundredGame, taken_by: Seat) -> FiveHundredGame:
    trick_cards = [card for card in game.round.cards_on_board.values() if card is not None]
    trick_points = sum([card.points.value for card in trick_cards])

    trick_winning_seats_info = game.round.seat_infos[taken_by]
    points_updated = trick_winning_seats_info.points + trick_points
    trick_count_updated = trick_winning_seats_info.trick_count + 1

    trick_winning_seats_info_updated = replace(
        trick_winning_seats_info,
        points=points_updated,
        trick_count=trick_count_updated,
    )

    cards_on_board_updated: dict[Seat, FiveHundredCard | None] = dict.fromkeys(game.round.cards_on_board, None)

    seat_infos_updated = dict(game.round.seat_infos) | {taken_by: trick_winning_seats_info_updated}

    prev_trick_updated = trick_cards

    round_updated = replace(
        game.round,
        cards_on_board=cards_on_board_updated,
        prev_trick=prev_trick_updated,
        required_suit=None,
        seat_infos=seat_infos_updated,
    )

    return replace(game, round=round_updated, active_seat=taken_by)
