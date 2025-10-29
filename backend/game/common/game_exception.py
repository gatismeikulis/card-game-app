from typing import Any, override
from core.exceptions.domain_exception import DomainException


class GameRulesException(DomainException):
    """Exception raised when a game rule is violated (can not apply a command on the current game state)"""

    code: str = "game_rules_error"
    detail: str = "A game rule violation occurred."

    @override
    def to_dict_minimal(self) -> dict[str, Any]:
        return self.to_dict()


class GameParsingException(DomainException):
    """Exception raised when a game parsing error occurs (can not parse raw data into game domain objects)"""

    code: str = "game_parsing_error"
    detail: str = "A game parsing error occurred."

    @override
    def to_dict_minimal(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "reason": self.reason,
            "context": self.context,
        }


class GameEngineException(DomainException):
    """Exception raised when a game engine error occurs (internal error in the game engine, wrong logic, etc.)"""

    code: str = "game_engine_error"
    detail: str = "A game engine error occurred."
