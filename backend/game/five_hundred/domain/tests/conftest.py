import pytest

from ....common.card import Suit, Rank
from ....common.seat import Seat
from ....common.hand import Hand
from ..five_hundred_phase import FiveHundredPhase
from ..five_hundred_round import FiveHundredRound
from ..five_hundred_seat_info import FiveHundredSeatInfo
from ..five_hundred_card import FiveHundredCard


@pytest.fixture
def sample_seats() -> frozenset[Seat]:
    return frozenset({Seat(1), Seat(2), Seat(3)})


@pytest.fixture
def sample_round(sample_seats: frozenset[Seat]) -> FiveHundredRound:
    return FiveHundredRound(
        seat_infos={
            seat: FiveHundredSeatInfo(hand=Hand(tuple()), bid=0, points=0, trick_count=0, marriage_points=[])
            for seat in sample_seats
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
