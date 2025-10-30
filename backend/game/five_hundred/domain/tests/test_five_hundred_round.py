import pytest

from ....common.hand import Hand
from ..five_hundred_seat_info import FiveHundredSeatInfo
from ..five_hundred_round import FiveHundredRound
from ..five_hundred_card import FiveHundredCard
from ..five_hundred_phase import FiveHundredPhase
from ....common.card import Suit, Rank
from ....common.seat import Seat


@pytest.fixture
def seats() -> frozenset[Seat]:
    return frozenset({Seat(1), Seat(2), Seat(3)})


@pytest.fixture
def round_in_progress(seats: frozenset[Seat]) -> FiveHundredRound:
    return FiveHundredRound(
        seat_infos={
            seat: FiveHundredSeatInfo(hand=Hand(tuple()), bid=0, points=0, trick_count=0, marriage_points=[])
            for seat in seats
        },
        cards_on_board={Seat(1): FiveHundredCard(Suit.CLUB, Rank.ACE), Seat(2): None, Seat(3): None},
        prev_trick=[
            FiveHundredCard(Suit.CLUB, Rank.ACE),
            FiveHundredCard(Suit.CLUB, Rank.KING),
            FiveHundredCard(Suit.CLUB, Rank.QUEEN),
        ],
        cards_to_take=[],
        required_suit=Suit.CLUB,
        trump_suit=Suit.SPADE,
        highest_bid=(Seat(1), 120),
        phase=FiveHundredPhase.PLAYING_CARDS,
        round_number=1,
        first_seat=Seat(1),
        is_marriage_announced=False,
    )


def test_create_initializes_empty_round(seats: frozenset[Seat]):
    round = FiveHundredRound.create(round_number=1, first_seat=Seat(1), taken_seats=seats)

    # Ensure all seats are represented
    assert set(round.seat_infos.keys()) == seats
    assert set(round.cards_on_board.keys()) == seats

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


def test_cards_on_board_count(round_in_progress: FiveHundredRound):
    assert round_in_progress.cards_on_board_count == 1


def test_to_dict_and_from_dict_roundtrip(round_in_progress: FiveHundredRound):
    data = round_in_progress.to_dict()
    restored = FiveHundredRound.from_dict(data)
    assert restored == round_in_progress
