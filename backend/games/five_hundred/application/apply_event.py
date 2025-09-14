from ..domain.five_hundred_event import FiveHundredEvent
from ..engine.add_marriage_points import add_marriage_points
from ..engine.finish_bidding import finish_bidding
from ..engine.finish_game import finish_game
from ..engine.finish_round import finish_round
from ..engine.play_card import play_card
from ..engine.take_hidden_cards import take_hidden_cards
from ..engine.pass_cards import pass_cards
from ..engine.make_bid import make_bid
from ..domain.five_hundred_game import FiveHundredGame
from ..engine.take_trick import take_trick


def apply_event(game: FiveHundredGame, event: FiveHundredEvent) -> FiveHundredGame:
    match event["type"]:
        case "BID_MADE":
            return make_bid(game, event["bid"])
        case "BIDDING_FINISHED":
            return finish_bidding(game)
        case "HIDDEN_CARDS_TAKEN":
            return take_hidden_cards(game)
        case "CARDS_PASSED":
            return pass_cards(game, event["card_to_next_seat"], event["card_to_prev_seat"])
        case "CARD_PLAYED":
            return play_card(game, event["card"])
        case "MARRIAGE_POINTS_ADDED":
            return add_marriage_points(game, event["points"], event["added_to"])
        case "TRICK_TAKEN":
            return take_trick(game, event["taken_by"])
        case "ROUND_FINISHED":
            return finish_round(game)
        case "GAME_FINISHED":
            return finish_game(game)
