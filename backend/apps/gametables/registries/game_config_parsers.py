from collections.abc import Mapping
from typing import Any, Callable

from game.common.game_config import GameConfig
from game.five_hundred.domain.five_hundred_game_config import FiveHundredGameConfig
from game.game_name import GameName

GAME_CONFIG_PARSERS: Mapping[GameName, Callable[[dict[str, Any]], GameConfig]] = {
    GameName.FIVE_HUNDRED: FiveHundredGameConfig.from_dict,
}


def get_game_config_parser(game_name: GameName) -> Callable[[dict[str, Any]], GameConfig]:
    return GAME_CONFIG_PARSERS[game_name]
