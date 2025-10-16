from dataclasses import replace

from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


def pass_cards(
    game: FiveHundredGame,
    card_to_next_seat: FiveHundredCard,
    card_to_prev_seat: FiveHundredCard,
) -> FiveHundredGame:
    active_seat = game.active_seat
    next_seat = active_seat.next()
    prev_seat = active_seat.prev()

    active_seats_info = game.active_seats_info
    next_seats_info = game.round.seat_infos[next_seat]
    prev_seats_info = game.round.seat_infos[prev_seat]

    active_seats_hand_updated = active_seats_info.hand.without_cards([card_to_next_seat, card_to_prev_seat])
    next_seats_hand_updated = next_seats_info.hand.with_added_cards([card_to_next_seat])
    prev_seats_hand_updated = prev_seats_info.hand.with_added_cards([card_to_prev_seat])

    active_seats_info_updated = replace(active_seats_info, hand=active_seats_hand_updated)
    next_seats_info_updated = replace(next_seats_info, hand=next_seats_hand_updated)
    prev_seats_info_updated = replace(prev_seats_info, hand=prev_seats_hand_updated)

    round_updated = replace(
        game.round,
        seat_infos={
            active_seat: active_seats_info_updated,
            next_seat: next_seats_info_updated,
            prev_seat: prev_seats_info_updated,
        },
        phase=FiveHundredPhase.PLAYING_CARDS,
    )

    return replace(game, round=round_updated)
