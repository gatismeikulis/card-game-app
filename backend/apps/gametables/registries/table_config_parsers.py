from collections.abc import Mapping
from typing import Any, Callable

from ..configs.five_hundred_table_config import FiveHundredTableConfig
from game.game_name import GameName
from ..domain.table_config import TableConfig

TABLE_CONFIG_PARSERS: Mapping[GameName, Callable[[dict[str, Any]], TableConfig]] = {
    GameName.FIVE_HUNDRED: FiveHundredTableConfig.from_dict,
}


def get_table_config_parser(game_name: GameName) -> Callable[[dict[str, Any]], TableConfig]:
    return TABLE_CONFIG_PARSERS[game_name]
