from enum import Enum


class BotStrategyKind(Enum):
    RANDOM = "RANDOM"

    @staticmethod
    def from_str(s: str) -> "BotStrategyKind":
        match s.upper():
            case "RANDOM":
                return BotStrategyKind.RANDOM
            case _:
                raise ValueError(f"Invalid bot strategy kind: {s}")
