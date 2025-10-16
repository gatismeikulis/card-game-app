from dataclasses import dataclass
from typing import Any

from game.common.bot_strategy import BotStrategy
from game.common.seat import SeatNumber


@dataclass(slots=True)
class Player:
    player_id: str
    seat_number: SeatNumber
    screen_name: str
    bot_strategy: BotStrategy | None = None  # when it is None, the player is human
    user_id: int | None = None  # if it's none, player is a bot
    # IMPORTANT: when adding new fields, consider adding them to the database model if needed for filtering/querying

    @property
    def is_bot(self) -> bool:
        return self.user_id is None

    @property
    def is_human(self) -> bool:
        return not self.is_bot

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "player_id": self.player_id,
            "seat_number": self.seat_number,
            "screen_name": self.screen_name,
            "bot_strategy_kind": self.bot_strategy.kind.value if self.bot_strategy else None,
            "user_id": self.user_id,
        }
