import pytest
from ..five_hundred_round_results import FiveHundredRoundResults
from ....common.seat import Seat


@pytest.fixture(
    params=[pytest.param((Seat(1), 100), id="with_bidding_results"), pytest.param(None, id="no_bidding_results")]
)
def round_results(request: pytest.FixtureRequest) -> FiveHundredRoundResults:
    return FiveHundredRoundResults(
        round_number=3,
        bidding_results=request.param,
        seat_points={Seat(1): 120, Seat(2): -100, Seat(3): -20},
    )


def test_to_dict_and_from_dict_roundtrip(round_results: FiveHundredRoundResults):
    data = round_results.to_dict()
    restored = FiveHundredRoundResults.from_dict(data)
    assert restored == round_results
