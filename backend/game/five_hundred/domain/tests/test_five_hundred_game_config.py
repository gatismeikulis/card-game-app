from typing import Any
import pytest
from ..five_hundred_game_config import FiveHundredGameConfig
from ....common.game_exception import GameParsingException, GameRulesException


def test_from_dict_with_valid_values():
    data = {"max_rounds": 50, "max_bid_no_marriage": 150, "min_bid": 80}
    config = FiveHundredGameConfig.from_dict(data)
    assert config.max_rounds == 50
    assert config.max_bid_no_marriage == 150
    assert config.min_bid == 80


def test_from_dict_with_missing_values_uses_defaults():
    config = FiveHundredGameConfig.from_dict({})
    assert config.max_rounds == 100
    assert config.max_bid_no_marriage == 120
    assert config.min_bid == 60


@pytest.mark.parametrize(
    "data,expected_exception",
    [
        ({"max_rounds": -10}, GameRulesException),
        ({"max_rounds": 600}, GameRulesException),
        ({"max_bid_no_marriage": 100}, GameRulesException),
        ({"max_bid_no_marriage": 250}, GameRulesException),
        ({"max_bid_no_marriage": -10}, GameRulesException),
        ({"min_bid": 50}, GameRulesException),
        ({"min_bid": 200}, GameRulesException),
        ({"max_rounds": "not-a-number"}, GameParsingException),
        ({"min_bid": "abc"}, GameParsingException),
        ({"max_bid_no_marriage": None}, GameParsingException),
    ],
)
def test_from_dict_invalid_values_raise(
    data: dict[str, Any], expected_exception: type[GameParsingException | GameRulesException]
):
    with pytest.raises(expected_exception):
        _ = FiveHundredGameConfig.from_dict(data)


def test_to_dict_and_from_dict_roundtrip():
    config = FiveHundredGameConfig(max_rounds=120, max_bid_no_marriage=150, min_bid=80)
    data = config.to_dict()
    restored = FiveHundredGameConfig.from_dict(data)
    assert restored == config
