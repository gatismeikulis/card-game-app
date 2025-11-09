from dataclasses import replace
import pytest

from ....common.card import Suit, Rank
from ....common.hand import Hand
from ....common.seat import Seat
from ...domain.five_hundred_game import FiveHundredGame
from ...domain.five_hundred_card import FiveHundredCard
from ...domain.five_hundred_seat_info import FiveHundredSeatInfo
from ..helpers import (
    get_next_seat_to_bid,
    get_round_ending_points_per_seat,
    has_marriage_in_hand,
    is_played_card_part_of_marriage,
    get_trick_winning_card,
)


@pytest.mark.parametrize(
    argnames="bid_by_seat_number, expected_next_seat_to_bid",
    # assuming active seat is always seat 1
    argvalues=[
        ({1: 0, 2: 0, 3: 0}, Seat(2)),
        ({1: -1, 2: -1, 3: -1}, None),
        ({1: 100, 2: -1, 3: -1}, None),
        ({1: -1, 2: -1, 3: 0}, Seat(3)),
        ({1: 160, 2: 120, 3: 140}, Seat(2)),
    ],
    ids=[
        "no_seats_have_bid",
        "all_seats_have_passed",
        "all_seats_have_passed_except_active_seat",
        "next_seat_has_passed",
        "all_seats_have_bid",
    ],
)
def test_get_next_seat_to_bid(
    sample_seat_infos: dict[Seat, FiveHundredSeatInfo],
    bid_by_seat_number: dict[int, int],
    expected_next_seat_to_bid: Seat | None,
):
    seat_infos = {seat: replace(info, bid=bid_by_seat_number[seat.number]) for seat, info in sample_seat_infos.items()}
    assert get_next_seat_to_bid(active_seat=Seat(1), seat_infos=seat_infos) == expected_next_seat_to_bid


@pytest.mark.parametrize(
    argnames="cards_to_add_to_sample_hand, expected_result",
    argvalues=[
        ([FiveHundredCard(Suit.CLUB, Rank.KING)], True),
        ([FiveHundredCard(Suit.SPADE, Rank.KING)], False),
        ([FiveHundredCard(Suit.CLUB, Rank.QUEEN)], False),
        ([], False),
    ],
    ids=[
        "has_king_queen_same_suit",
        "has_king_queen_different_suits",
        "has_two_queens_of_same_suit",
        "has_single_queen",
    ],
)
def test_has_marriage_in_hand(
    sample_hand: Hand[FiveHundredCard], cards_to_add_to_sample_hand: list[FiveHundredCard], expected_result: bool
):
    hand = sample_hand.with_added_cards(cards_to_add_to_sample_hand)
    assert has_marriage_in_hand(hand) == expected_result


@pytest.mark.parametrize(
    argnames="played_card, cards_to_add_to_sample_hand, expected_result",
    argvalues=[
        (FiveHundredCard(Suit.CLUB, Rank.KING), [], True),
        (FiveHundredCard(Suit.SPADE, Rank.QUEEN), [FiveHundredCard(Suit.SPADE, Rank.KING)], True),
        (FiveHundredCard(Suit.DIAMOND, Rank.KING), [], False),
        (FiveHundredCard(Suit.HEART, Rank.QUEEN), [], False),
    ],
    ids=[
        "played_card_is_king_and_remaining_cards_have_same_suit_queen",
        "played_card_is_queen_and_remaining_cards_have_same_suit_king",
        "played_card_is_king_and_remaining_cards_have_queen_of_different_suit",
        "playerd_card_is_queen_and_remaining_cards_do_not_have_any_king",
    ],
)
def test_is_played_card_part_of_marriage(
    sample_hand: Hand[FiveHundredCard],
    played_card: FiveHundredCard,
    cards_to_add_to_sample_hand: list[FiveHundredCard],
    expected_result: bool,
):
    hand = sample_hand.with_added_cards(cards_to_add_to_sample_hand)
    assert is_played_card_part_of_marriage(played_card, list(hand.cards)) == expected_result


def test_get_trick_winning_card_prefers_highest_trump():
    trick = [
        FiveHundredCard(Suit.HEART, Rank.TEN),
        FiveHundredCard(Suit.SPADE, Rank.ACE),
        FiveHundredCard(Suit.SPADE, Rank.JACK),
    ]
    winning_card = get_trick_winning_card(trick, required_suit=Suit.HEART, trump_suit=Suit.SPADE)
    assert winning_card == FiveHundredCard(Suit.SPADE, Rank.ACE)


def test_get_trick_winning_card_no_trumps_on_board():
    trick = [
        FiveHundredCard(Suit.HEART, Rank.JACK),
        FiveHundredCard(Suit.SPADE, Rank.KING),
        FiveHundredCard(Suit.HEART, Rank.ACE),
    ]
    winning_card = get_trick_winning_card(trick, required_suit=Suit.HEART, trump_suit=Suit.CLUB)
    assert winning_card == FiveHundredCard(Suit.HEART, Rank.ACE)


def test_get_trick_winning_card_tiny_trump_wins_big_cards():
    trick = [
        FiveHundredCard(Suit.HEART, Rank.NINE),
        FiveHundredCard(Suit.SPADE, Rank.KING),
        FiveHundredCard(Suit.DIAMOND, Rank.ACE),
    ]
    winning_card = get_trick_winning_card(trick, required_suit=Suit.DIAMOND, trump_suit=Suit.HEART)
    assert winning_card == FiveHundredCard(Suit.HEART, Rank.NINE)


@pytest.mark.parametrize(
    "highest_bid,round_points_per_seat_number,declarer_gave_up, expected_points_per_seat",
    [
        (None, {1: 0, 2: 0, 3: 0}, False, {Seat(1): 0, Seat(2): 0, Seat(3): 0}),
        ((Seat(2), 95), {1: 24, 2: 96, 3: 0}, False, {Seat(1): -25, Seat(2): -95, Seat(3): 0}),
        ((Seat(2), 120), {1: 17, 2: 85, 3: 18}, False, {Seat(1): -15, Seat(2): 120, Seat(3): -20}),
        ((Seat(1), 100), {1: 0, 2: 0, 3: 0}, True, {Seat(1): 100, Seat(2): -50, Seat(3): -50}),
    ],
    ids=["all_passed", "declarer_exceeds_the_bid", "declarer_fails_to_exceed_the_bid", "declarer_gives_up"],
)
def test_get_round_ending_points_per_seat(
    sample_game: FiveHundredGame,
    highest_bid: tuple[Seat, int] | None,
    round_points_per_seat_number: dict[int, int],
    declarer_gave_up: bool,
    expected_points_per_seat: dict[int, int],
):
    sample_round = sample_game.round
    sample_seat_infos = sample_game.round.seat_infos
    sample_seat_infos_updated = {
        seat: replace(seat_info, points=round_points_per_seat_number[seat.number])
        for seat, seat_info in sample_seat_infos.items()
    }
    sample_round_updated = replace(sample_round, seat_infos=sample_seat_infos_updated, highest_bid=highest_bid)
    sample_game_updated = replace(sample_game, round=sample_round_updated)
    round_ending_points_per_seat = get_round_ending_points_per_seat(
        sample_game_updated, has_declarer_given_up=declarer_gave_up
    )

    assert round_ending_points_per_seat == expected_points_per_seat
