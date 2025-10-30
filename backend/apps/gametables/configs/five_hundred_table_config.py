from dataclasses import dataclass
from typing import Any, Self, override

from ..exceptions import GameTableRulesException
from game.common.game_exception import GameParsingException
from game.five_hundred.domain.constants import MAX_SEATS, MIN_SEATS
from ..domain.table_config import TableConfig


@dataclass(frozen=True, slots=True)
class FiveHundredTableConfig(TableConfig):
    @override
    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "automatic_start": self.automatic_start,
            "bots_allowed": self.bots_allowed,
            "min_seats": self.min_seats,
            "max_seats": self.max_seats,
        }

    @override
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        try:
            automatic_start = bool(data.get("automatic_start", True))
            bots_allowed = bool(data.get("bots_allowed", True))
            min_seats = int(data.get("min_seats", MIN_SEATS))
            max_seats = int(data.get("max_seats", MAX_SEATS))
        except Exception:
            raise GameParsingException(
                reason="config_parsing_error", detail=f"Could not create FiveHundredTableConfig from input: {data}"
            )
        if min_seats < MIN_SEATS or max_seats > MAX_SEATS:
            raise GameTableRulesException(detail=f"min_seats and max_seats must be between {MIN_SEATS} and {MAX_SEATS}")
        return cls(
            automatic_start=automatic_start,
            bots_allowed=bots_allowed,
            min_seats=min_seats,
            max_seats=max_seats,
        )
