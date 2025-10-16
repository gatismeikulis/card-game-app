from collections.abc import Mapping

from game.game_name import GameName
from game.common.game_event_parser import GameEventParser
from game.five_hundred.five_hundred_event_parser import FiveHundredEventParser

GAME_EVENT_PARSERS: Mapping[GameName, GameEventParser] = {
    GameName.FIVE_HUNDRED: FiveHundredEventParser(),
}


def get_game_event_parser(game_name: GameName) -> GameEventParser:
    return GAME_EVENT_PARSERS[game_name]
