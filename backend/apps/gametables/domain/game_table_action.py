from enum import Enum

from ..exceptions import GameTableRulesException


class GameTableAction(Enum):
    TAKE_REGULAR_TURN = "take-regular-turn"
    TAKE_AUTOMATIC_TURN = "take_automatic_turn"
    JOIN_TABLE = "join"
    LEAVE_TABLE = "leave"
    ADD_BOT = "add-bot"
    REMOVE_BOT = "remove-bot"
    START_GAME = "start-game"

    @staticmethod
    def from_str(s: str) -> "GameTableAction":
        match s.upper():
            case "TAKE_REGULAR_TURN":
                return GameTableAction.TAKE_REGULAR_TURN
            case "TAKE_AUTOMATIC_TURN":
                return GameTableAction.TAKE_AUTOMATIC_TURN
            case "JOIN_TABLE":
                return GameTableAction.JOIN_TABLE
            case "LEAVE_TABLE":
                return GameTableAction.LEAVE_TABLE
            case "ADD_BOT":
                return GameTableAction.ADD_BOT
            case "REMOVE_BOT":
                return GameTableAction.REMOVE_BOT
            case "START_GAME":
                return GameTableAction.START_GAME
            case _:
                raise GameTableRulesException(
                    reason="game_table_action_parsing_error",
                    detail=f"Could not parse game table action from input: {s}",
                )
