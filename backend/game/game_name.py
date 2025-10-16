from enum import Enum


class GameName(Enum):
    FIVE_HUNDRED = "five_hundred"

    @staticmethod
    def from_str(s: str) -> "GameName":
        match s.upper():
            case "FIVE_HUNDRED":
                return GameName.FIVE_HUNDRED
            case _:
                raise ValueError(f"Invalid game name: {s}")
