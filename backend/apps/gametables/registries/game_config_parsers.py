from collections.abc import Mapping

from game.common.game_config_parser import GameConfigParser
from game.five_hundred.domain.five_hundred_game_config import FiveHundredGameConfigParser
from game.game_name import GameName

GAME_CONFIG_PARSERS: Mapping[GameName, GameConfigParser] = {
    GameName.FIVE_HUNDRED: FiveHundredGameConfigParser(),
}


def get_game_config_parser(game_name: GameName) -> GameConfigParser:
    return GAME_CONFIG_PARSERS[game_name]
