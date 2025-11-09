from collections.abc import Mapping, Sequence

from ...common.hand import Hand
from ...common.card import Rank, Suit
from ...common.seat import Seat
from ..domain.constants import MUST_BID_THRESHOLD
from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_game import FiveHundredGame
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


def get_round_ending_points_per_seat(game: FiveHundredGame, has_declarer_given_up: bool = False) -> Mapping[Seat, int]:
    bidding_winning_seat = game.round.highest_bid[0] if game.round.highest_bid else None

    def get_round_points_for_seat(seat: Seat, seats_game_points: int) -> int:
        points_from_tricks = game.round.seat_infos[seat].points
        if bidding_winning_seat == seat:
            winning_bid = game.round.highest_bid[1] if game.round.highest_bid else 0
            return (
                winning_bid if winning_bid <= points_from_tricks else -winning_bid
            )  # this logic is correct also after giving up
        else:
            points = game.game_config.give_up_points if has_declarer_given_up else points_from_tricks
            diff_of_five = points_from_tricks % 5
            points_rounded = points - diff_of_five + 5 if diff_of_five > 2 else points - diff_of_five
            return points_rounded if seats_game_points >= MUST_BID_THRESHOLD else 0

    return {seat: -get_round_points_for_seat(seat, game.summary[seat]) for seat in game.taken_seats}
