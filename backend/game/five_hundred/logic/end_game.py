from dataclasses import replace

from ...common.game_ending import GameEnding, GameEndingReason
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


def end_game(game: FiveHundredGame) -> FiveHundredGame:
    round_updated = replace(
        game.round,
        phase=FiveHundredPhase.GAME_ENEDED,
        seat_infos={},
        cards_on_board={},
        cards_to_take=[],
        required_suit=None,
        trump_suit=None,
        highest_bid=None,
        round_number=0,
        is_marriage_announced=False,
    )
    return replace(
        game,
        round=round_updated,
        ending=GameEnding(winners=[], losers=[], reason=GameEndingReason.FINISHED, point_differences={}),
    )
