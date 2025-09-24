from dataclasses import replace

from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


def finish_bidding(game: FiveHundredGame) -> FiveHundredGame:
    round_updated = replace(game.round, phase=FiveHundredPhase.FORMING_HANDS)
    return replace(game, round=round_updated)
