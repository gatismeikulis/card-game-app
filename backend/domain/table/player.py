from dataclasses import dataclass

from backend.domain.game.common.bot_strategy import BotStrategy
from backend.domain.game.common.seat import SeatNumber


@dataclass(slots=True)
class Player:
    seat_number: SeatNumber
    agreed_to_start: bool = False
    bot_strategy: BotStrategy | None = None  # when it is None, the player is human
