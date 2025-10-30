from dataclasses import dataclass
from typing import Any, Self, override

from ...common.game_exception import GameParsingException, GameRulesException
from ...common.game_config import GameConfig


@dataclass(frozen=True, slots=True)
class FiveHundredGameConfig(GameConfig):
    max_rounds: int  # default = 100 (range: 20 - 500)
    max_bid_no_marriage: int  # default = 120 (range: 120 - 200)
    min_bid: int  # default = 60 (range: 60 - 120)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "max_rounds": self.max_rounds,
            "max_bid_no_marriage": self.max_bid_no_marriage,
            "min_bid": self.min_bid,
        }

    @override
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        try:
            max_rounds = int(data.get("max_rounds", 100))
            max_bid_no_marriage = int(data.get("max_bid_no_marriage", 120))
            min_bid = int(data.get("min_bid", 60))
        except Exception:
            raise GameParsingException(
                reason="config_parsing_error", detail=f"Could not create FiveHundredGameConfig from input: {data}"
            )

        if max_rounds < 20 or max_rounds > 500:
            raise GameRulesException(detail="max_rounds setting must be between 20 and 500")
        if max_bid_no_marriage < 120 or max_bid_no_marriage > 200:
            raise GameRulesException(detail="max_bid_no_marriage setting must be between 120 and 200")
        if min_bid < 60 or min_bid > 120:
            raise GameRulesException(detail="min_bid setting must be between 60 and 120")
        return cls(
            max_rounds=max_rounds,
            max_bid_no_marriage=max_bid_no_marriage,
            min_bid=min_bid,
        )
