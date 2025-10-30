import pytest

from ....common.card import Rank, Suit
from ....common.seat import Seat
from ....common.hand import Hand
from ...domain.five_hundred_card import FiveHundredCard
from ...domain.five_hundred_seat_info import FiveHundredSeatInfo


@pytest.fixture
def sample_seats() -> frozenset[Seat]:
    return frozenset({Seat(1), Seat(2), Seat(3)})


@pytest.fixture
def sample_seat_infos(sample_seats: frozenset[Seat]) -> dict[Seat, FiveHundredSeatInfo]:
    # empty seat infos
    return {
        seat: FiveHundredSeatInfo(
            hand=Hand(tuple()),
            bid=0,
            points=0,
            trick_count=0,
            marriage_points=[],
        )
        for seat in sample_seats
    }


@pytest.fixture
def sample_hand() -> Hand[FiveHundredCard]:
    """[9c, Tc, Jc, Qc]"""
    return Hand[FiveHundredCard](
        cards=(
            FiveHundredCard(Suit.CLUB, Rank.NINE),
            FiveHundredCard(Suit.CLUB, Rank.TEN),
            FiveHundredCard(Suit.CLUB, Rank.JACK),
            FiveHundredCard(Suit.CLUB, Rank.QUEEN),
        )
    )
