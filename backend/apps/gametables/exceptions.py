from typing import Any, override
from core.exceptions.domain_exception import DomainException


class GameTableRulesException(DomainException):
    """Exception raised when a game table rules violation occurs (can not perfom an action because it's against the rules/configuration of the game table or not applicable to the current game state)"""

    code: str = "game_table_rules_error"
    detail: str = "A game table rules violation occurred."

    @override
    def to_dict_minimal(self) -> dict[str, Any]:
        return self.to_dict()


class GameTableInternalException(DomainException):
    """Exception raised when a game table internal error occurs (internal error in the game table, wrong logic, etc.)"""

    code: str = "game_table_internal_error"
    detail: str = "A game table internal error occurred."
