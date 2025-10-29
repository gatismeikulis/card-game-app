from enum import Enum

from .common.game_exception import GameParsingException


class BotStrategyKind(Enum):
    RANDOM = "RANDOM"

    @staticmethod
    def from_str(s: str) -> "BotStrategyKind":
        match s.upper():
            case "RANDOM":
                return BotStrategyKind.RANDOM
            case _:
                raise GameParsingException(
                    reason="bot_strategy_kind_parsing_error",
                    detail=f"Could not parse bot strategy kind from input: {s}",
                )
