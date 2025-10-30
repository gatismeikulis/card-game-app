import pytest

from ....common.seat import Seat
from ....common.game_exception import GameEngineException
from ...domain.constants import GAME_STARTING_POINTS
from ..five_hundred_game import FiveHundredGame
from ..five_hundred_game_config import FiveHundredGameConfig
from ..five_hundred_round import FiveHundredRound


@pytest.fixture
def sample_game_config() -> FiveHundredGameConfig:
    return FiveHundredGameConfig(max_rounds=100, max_bid_no_marriage=120, min_bid=60)


@pytest.fixture
def sample_game(
    sample_game_config: FiveHundredGameConfig, sample_seats: frozenset[Seat], sample_round: FiveHundredRound
) -> FiveHundredGame:
    return FiveHundredGame(
        is_finished=False,
        game_config=sample_game_config,
        taken_seats=sample_seats,
        round=sample_round,
        results=[],
        summary={seat: GAME_STARTING_POINTS for seat in sample_seats},
        active_seat=sample_round.first_seat,
    )


def test_init_requires_game_specific_game_config(sample_seats: frozenset[Seat]):
    with pytest.raises(GameEngineException):
        _ = FiveHundredGame.init(
            game_config="not-a-config", taken_seat_numbers=frozenset(seat.number for seat in sample_seats)
        )


def test_init_sets_correct_properties(sample_game_config: FiveHundredGameConfig, sample_seats: frozenset[Seat]):
    game = FiveHundredGame.init(sample_game_config, frozenset(seat.number for seat in sample_seats))
    expected_round = FiveHundredRound.create(round_number=1, first_seat=Seat(1), taken_seats=sample_seats)
    assert game.is_finished is False
    assert game.game_config == sample_game_config
    assert game.taken_seats == sample_seats
    assert game.active_seat in game.taken_seats
    assert game.round == expected_round
    assert game.summary == {seat: GAME_STARTING_POINTS for seat in sample_seats}
    assert game.results == []


def test_winners_property_only_available_when_game_is_finished(sample_game: FiveHundredGame):
    with pytest.raises(GameEngineException):
        _ = sample_game.winners


def test_to_dict_and_from_dict_roundtrip(sample_game: FiveHundredGame):
    data = sample_game.to_dict()
    restored = FiveHundredGame.from_dict(data)
    assert restored == sample_game


def test_to_public_dict_hides_private_and_non_essential_info(sample_game: FiveHundredGame):
    public_data = sample_game.to_public_dict(seat_number=1)

    assert "cards_to_take" not in public_data["round"]
    # make sure that non-essential information for UI is also not included
    assert "results" not in public_data
    assert "game_config" not in public_data
    assert "taken_seats" not in public_data
