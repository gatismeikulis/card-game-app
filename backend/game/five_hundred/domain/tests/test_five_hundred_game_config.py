from typing import Any
import pytest
from ..five_hundred_game_config import FiveHundredGameConfig
from ....common.game_exception import GameParsingException, GameRulesException


def test_from_dict_with_valid_values():
    data = {"max_rounds": 50, "max_bid_no_marriage": 150, "min_bid": 80, "give_up_points": 50}
    config = FiveHundredGameConfig.from_dict(data)
    assert config.max_rounds == 50
    assert config.max_bid_no_marriage == 150
    assert config.min_bid == 80
    assert config.give_up_points == 50


def test_from_dict_with_missing_values_uses_defaults():
    config = FiveHundredGameConfig.from_dict({})
    assert (config.max_rounds, config.max_bid_no_marriage, config.min_bid, config.give_up_points) == (100, 120, 60, 50)


@pytest.mark.parametrize(
    argnames="data,expected_exception",
    argvalues=[
        pytest.param({"max_rounds": -10}, GameRulesException, id="max_rounds_too_low"),
        pytest.param({"max_rounds": 600}, GameRulesException, id="max_rounds_too_high"),
        pytest.param({"max_bid_no_marriage": 100}, GameRulesException, id="max_bid_no_marriage_too_low"),
        pytest.param({"max_bid_no_marriage": 250}, GameRulesException, id="max_bid_no_marriage_too_high"),
        pytest.param({"min_bid": 50}, GameRulesException, id="min_bid_too_low"),
        pytest.param({"min_bid": 200}, GameRulesException, id="min_bid_too_high"),
        pytest.param({"max_rounds": "not-a-number"}, GameParsingException, id="max_rounds_not_numeric"),
        pytest.param({"min_bid": "abc"}, GameParsingException, id="min_bid_not_numeric"),
        pytest.param({"max_bid_no_marriage": None}, GameParsingException, id="max_bid_no_marriage_not_numeric"),
        pytest.param({"give_up_points": 10}, GameRulesException, id="give_up_points_too_low"),
        pytest.param({"give_up_points": 150}, GameRulesException, id="give_up_points_too_high"),
        pytest.param({"give_up_points": "not-a-number"}, GameParsingException, id="give_up_points_not_numeric"),
    ],
)
def test_from_dict_invalid_values_raise(
    data: dict[str, Any],
    expected_exception: type[Exception],
):
    with pytest.raises(expected_exception):
        _ = FiveHundredGameConfig.from_dict(data)


def test_to_dict_and_from_dict_roundtrip():
    config = FiveHundredGameConfig(max_rounds=120, max_bid_no_marriage=150, min_bid=80, give_up_points=50)
    data = config.to_dict()
    restored = FiveHundredGameConfig.from_dict(data)
    assert restored == config
