from dataclasses import replace

from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_game import FiveHundredGame


def play_card(game: FiveHundredGame, card: FiveHundredCard) -> FiveHundredGame:
    cards_on_board_count = game.round.cards_on_board_count

    cards_on_board_updated = dict(game.round.cards_on_board) | {game.active_seat: card}

    active_seat = game.active_seat
    active_seats_info = game.active_seats_info
    active_seats_hand_updated = active_seats_info.hand.without_cards([card])

    active_seats_info_updated = replace(active_seats_info, hand=active_seats_hand_updated)

    # 1st card played for this trick (cards on board is empty)
    if cards_on_board_count == 0:
        required_suit_updated = card.suit
        trump_suit_updated = card.suit if game.round.trump_suit is None else game.round.trump_suit

        seat_infos_updated = dict(game.round.seat_infos) | {active_seat: active_seats_info_updated}

        round_updated = replace(
            game.round,
            cards_on_board=cards_on_board_updated,
            seat_infos=seat_infos_updated,
            required_suit=required_suit_updated,
            trump_suit=trump_suit_updated,
        )

        return replace(game, round=round_updated, active_seat=active_seat.next())

    # 2nd or 3rd card played for this trick
    else:
        seat_infos_updated = dict(game.round.seat_infos) | {active_seat: active_seats_info_updated}

        round_updated = replace(
            game.round,
            cards_on_board=cards_on_board_updated,
            seat_infos=seat_infos_updated,
        )

        return replace(game, round=round_updated, active_seat=active_seat.next())
