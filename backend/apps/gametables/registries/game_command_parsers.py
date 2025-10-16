from collections.abc import Mapping

from game.common.game_command_parser import GameCommandParser
from game.five_hundred.five_hundred_command_parser import FiveHundredCommandParser
from game.game_name import GameName

GAME_COMMAND_PARSERS: Mapping[GameName, GameCommandParser] = {
    GameName.FIVE_HUNDRED: FiveHundredCommandParser(),
}


def get_command_parser(game_name: GameName) -> GameCommandParser:
    return GAME_COMMAND_PARSERS[game_name]
