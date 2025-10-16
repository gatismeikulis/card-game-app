from collections.abc import Mapping

from game.five_hundred.domain.five_hundred_game import FiveHundredGame
from game.common.game_state import GameState
from game.game_name import GameName

GAME_CLASSES: Mapping[GameName, type[GameState]] = {
    GameName.FIVE_HUNDRED: FiveHundredGame,
}


def get_game_class(game_name: GameName) -> type[GameState]:
    return GAME_CLASSES[game_name]
