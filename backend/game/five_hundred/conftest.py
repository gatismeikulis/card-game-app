import pytest

from ..common.card import Rank, Suit
from ..common.seat import Seat
from ..common.hand import Hand
from .domain.five_hundred_card import FiveHundredCard
from .domain.five_hundred_seat_info import FiveHundredSeatInfo
from .domain.five_hundred_round import FiveHundredRound
from .domain.five_hundred_phase import FiveHundredPhase
from .domain.five_hundred_game import FiveHundredGame
from .domain.five_hundred_game_config import FiveHundredGameConfig
from .domain.constants import GAME_STARTING_POINTS


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


@pytest.fixture
def sample_round(sample_seat_infos: dict[Seat, FiveHundredSeatInfo]) -> FiveHundredRound:
    return FiveHundredRound(
        seat_infos=sample_seat_infos,
        cards_on_board={Seat(1): None, Seat(2): None, Seat(3): None},
        prev_trick=[],
        cards_to_take=[],
        required_suit=None,
        trump_suit=None,
        highest_bid=(Seat(1), 100),
        phase=FiveHundredPhase.INITIALIZING,
        round_number=1,
        first_seat=Seat(1),
        is_marriage_announced=False,
    )


@pytest.fixture
def sample_game_config() -> FiveHundredGameConfig:
    return FiveHundredGameConfig(max_rounds=100, max_bid_no_marriage=120, min_bid=60, give_up_points=50)


@pytest.fixture
def sample_game(
    sample_seats: frozenset[Seat], sample_round: FiveHundredRound, sample_game_config: FiveHundredGameConfig
) -> FiveHundredGame:
    return FiveHundredGame(
        round=sample_round,
        results=[],
        summary={seat: GAME_STARTING_POINTS for seat in sample_seats},
        active_seat=sample_round.first_seat,
        ending=None,
        game_config=sample_game_config,
        taken_seats=sample_seats,
        turn_number=0,
    )
