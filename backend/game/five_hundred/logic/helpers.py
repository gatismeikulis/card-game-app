from collections.abc import Mapping, Sequence

from ...common.hand import Hand
from ...common.card import Rank, Suit
from ...common.seat import Seat
from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_seat_info import FiveHundredSeatInfo


def get_next_seat_to_bid(
    active_seat: Seat,
    seat_infos: Mapping[Seat, FiveHundredSeatInfo],
) -> Seat | None:
    next_seat = active_seat.next(seat_infos.keys())
    prev_seat = active_seat.prev(seat_infos.keys())

    next_seats_latest_bid = seat_infos[next_seat].bid
    prev_seats_latest_bid = seat_infos[prev_seat].bid

    next_seat_to_bid: Seat | None = None

    if next_seats_latest_bid >= 0:
        next_seat_to_bid = next_seat
    elif prev_seats_latest_bid >= 0:
        next_seat_to_bid = prev_seat
    else:
        next_seat_to_bid = None

    return next_seat_to_bid


def has_marriage_in_hand(hand: Hand[FiveHundredCard]) -> bool:
    suits: dict[Suit, dict[Rank, bool]] = {}

    for card in hand.cards:
        suit, rank = card.suit, card.rank

        if suit not in suits:
            suits[suit] = {Rank.KING: False, Rank.QUEEN: False}

        if rank == Rank.KING:
            suits[suit][Rank.KING] = True
        elif rank == Rank.QUEEN:
            suits[suit][Rank.QUEEN] = True

        if suits[suit][Rank.KING] and suits[suit][Rank.QUEEN]:
            return True

    return False


def is_played_card_part_of_marriage(
    played_card: FiveHundredCard, cards_left_in_hand: Sequence[FiveHundredCard]
) -> bool:
    if played_card.rank == Rank.QUEEN:
        return FiveHundredCard(played_card.suit, Rank.KING) in cards_left_in_hand
    elif played_card.rank == Rank.KING:
        return FiveHundredCard(played_card.suit, Rank.QUEEN) in cards_left_in_hand
    return False


def get_trick_winning_card(
    trick_cards: Sequence[FiveHundredCard],
    required_suit: Suit | None,
    trump_suit: Suit | None,
) -> FiveHundredCard:
    """
    Rules:
    1. If trump cards are played, highest trump wins
    2. Otherwise, highest card of required suit wins

    """
    trump_cards_played = [card for card in trick_cards if card.suit == trump_suit]
    if len(trump_cards_played) > 0:
        trump_cards_played.sort(key=lambda c: c.strength().value, reverse=True)
        return trump_cards_played[0]
    else:
        required_suit_cards_played = [card for card in trick_cards if card.suit == required_suit]
        required_suit_cards_played.sort(key=lambda c: c.strength().value, reverse=True)
        return required_suit_cards_played[0]
