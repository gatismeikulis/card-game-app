from dataclasses import replace

from ..domain.five_hundred_game import FiveHundredGame


def give_up(game: FiveHundredGame) -> FiveHundredGame:
    turn_number_updated = game.turn_number + 1
    return replace(game, turn_number=turn_number_updated)
