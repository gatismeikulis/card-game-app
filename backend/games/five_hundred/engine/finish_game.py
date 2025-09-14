from dataclasses import replace

from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


def finish_game(game: FiveHundredGame) -> FiveHundredGame:

    round_updated = replace(
        game.round,
        _phase=FiveHundredPhase.GAME_FINISHED,
        _seat_infos={},
        _cards_on_board={},
        _cards_to_take=[],
        _required_suit=None,
        _trump_suit=None,
        _highest_bid=None,
        _active_seat=None,
        _round_number=0,
        _first_seat=None,
        _is_marriage_announced=False,
    )
    return replace(game, _round=round_updated)
