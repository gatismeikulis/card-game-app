from collections.abc import Mapping

from game.game_name import GameName
from game.common.game_engine import GameEngine
from game.five_hundred.five_hundred_game_engine import FiveHundredGameEngine

GAME_ENGINES: Mapping[GameName, GameEngine] = {
    GameName.FIVE_HUNDRED: FiveHundredGameEngine(),
}


def get_game_engine(game_name: GameName) -> GameEngine:
    return GAME_ENGINES[game_name]
