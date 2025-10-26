from core.exceptions.domain_exception import DomainException


class GameTableRulesException(DomainException):
    """Exception raised when a game table rules violation occurs (can not perfom an action because it's against the rules/configuration of the game table or not applicable to the current game state)"""

    code: str = "game_table_rules_error"
    message: str = "A game table rules violation occurred."


class GameTableInternalException(DomainException):
    """Exception raised when a game table internal error occurs (internal error in the game table, wrong logic, etc.)"""

    code: str = "game_table_internal_error"
    message: str = "A game table internal error occurred."
