from dataclasses import replace

from ....common.card import Rank, Suit
from ....common.seat import Seat
from ..five_hundred_card import FiveHundredCard
from ..five_hundred_round import FiveHundredRound
from ..five_hundred_phase import FiveHundredPhase


def test_create_initializes_empty_round(sample_seats: frozenset[Seat]):
    round = FiveHundredRound.create(round_number=1, first_seat=Seat(1), taken_seats=sample_seats)

    # Ensure all seats are represented
    assert set(round.seat_infos.keys()) == sample_seats
    assert set(round.cards_on_board.keys()) == sample_seats

    # Ensure each seat has default empty info
    for info in round.seat_infos.values():
        assert info.bid == 0
        assert info.points == 0
        assert info.trick_count == 0
        assert info.hand.cards == tuple()
        assert info.marriage_points == []

    # Check default state
    assert round.phase == FiveHundredPhase.INITIALIZING
    assert round.cards_on_board_count == 0
    assert round.required_suit is None
    assert round.trump_suit is None
    assert round.highest_bid is None
    assert round.is_marriage_announced is False


def test_cards_on_board_count(sample_round: FiveHundredRound):
    sample_round_updated = replace(sample_round, cards_on_board={Seat(1): FiveHundredCard(Suit.CLUB, Rank.ACE)})
    assert sample_round_updated.cards_on_board_count == 1


def test_to_dict_and_from_dict_roundtrip(sample_round: FiveHundredRound):
    data = sample_round.to_dict()
    restored = FiveHundredRound.from_dict(data)
    assert restored == sample_round
