from enum import Enum

from .common.game_exception import GameParsingException


class GameName(Enum):
    FIVE_HUNDRED = "five_hundred"

    @staticmethod
    def from_str(s: str) -> "GameName":
        match s.upper():
            case "FIVE_HUNDRED":
                return GameName.FIVE_HUNDRED
            case _:
                raise GameParsingException(
                    reason="game_name_parsing_error", message=f"Could not parse game name from input: {s}"
                )
