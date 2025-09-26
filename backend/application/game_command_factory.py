from typing import Any

from backend.domain.game.common.command import Command
from backend.domain.game.five_hundred.five_hundred_command_factory import (
    FiveHundredCommandFactory,
)
from backend.domain.game.game_name import GameName


class GameCommandFactory:
    @staticmethod
    def create(game_name: GameName, raw_command: dict[str, Any]) -> Command:
        match game_name:
            case GameName.FIVE_HUNDRED:
                return FiveHundredCommandFactory.from_json(raw_command)
