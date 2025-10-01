from typing import Any, final

from backend.domain.game.common.game_command import GameCommand
from backend.domain.game.common.game_command_parser import GameCommandParser
from backend.domain.game.five_hundred.five_hundred_command_parser import FiveHundredCommandParser
from backend.domain.game.game_name import GameName


@final
class GameCommandParsingService:
    def __init__(self) -> None:
        self._command_parsers: dict[GameName, GameCommandParser] = {
            GameName.FIVE_HUNDRED: FiveHundredCommandParser(),
        }

    def parse(self, game_name: GameName, raw_command: dict[str, Any]) -> GameCommand:
        return self._command_parsers[game_name].from_dict(raw_command)
