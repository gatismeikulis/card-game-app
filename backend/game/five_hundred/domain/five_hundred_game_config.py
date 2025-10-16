from dataclasses import dataclass
from typing import Any, override

from ...common.game_config import GameConfig


@dataclass(frozen=True, slots=True)
class FiveHundredGameConfig(GameConfig):
    min_seats: int
    max_seats: int

    @override
    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {"min_seats": self.min_seats, "max_seats": self.max_seats}


class FiveHundredGameConfigParser:
    def from_dict(self, raw_config: dict[str, Any]) -> GameConfig:
        # TODO validate that max seats is not greater than min seats etc.
        min_seats = raw_config.get("min_seats", 3)
        max_seats = raw_config.get("max_seats", 3)
        return FiveHundredGameConfig(min_seats=min_seats, max_seats=max_seats)
