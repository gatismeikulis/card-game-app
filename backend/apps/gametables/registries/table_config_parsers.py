from collections.abc import Mapping

from ..configs.five_hundred_table_config import FiveHundredTableConfigParser
from ..domain.table_config_parser import TableConfigParser
from game.game_name import GameName

TABLE_CONFIG_PARSERS: Mapping[GameName, TableConfigParser] = {
    GameName.FIVE_HUNDRED: FiveHundredTableConfigParser(),
}


def get_table_config_parser(game_name: GameName) -> TableConfigParser:
    return TABLE_CONFIG_PARSERS[game_name]
