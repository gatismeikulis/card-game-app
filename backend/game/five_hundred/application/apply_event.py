from ..domain.five_hundred_event import (
    DeckShuffledEvent,
    BiddingFinishedEvent,
    BidMadeEvent,
    CardPlayedEvent,
    CardsPassedEvent,
    FiveHundredEvent,
    GameFinishedEvent,
    DeclarerGaveUpEvent,
    HiddenCardsTakenEvent,
    MarriagePointsAddedEvent,
    RoundFinishedEvent,
    TrickTakenEvent,
)
from ..domain.five_hundred_game import FiveHundredGame
from ..logic.add_marriage_points import add_marriage_points
from ..logic.deal_cards import deal_cards
from ..logic.finish_bidding import finish_bidding
from ..logic.finish_game import finish_game
from ..logic.finish_round import finish_round
from ..logic.make_bid import make_bid
from ..logic.pass_cards import pass_cards
from ..logic.play_card import play_card
from ..logic.take_hidden_cards import take_hidden_cards
from ..logic.take_trick import take_trick


def apply_event(game: FiveHundredGame, event: FiveHundredEvent) -> FiveHundredGame:
    match event:
        case DeckShuffledEvent(deck=deck):
            return deal_cards(game, deck)
        case BidMadeEvent(bid=bid):
            return make_bid(game, bid)
        case BiddingFinishedEvent():
            return finish_bidding(game)
        case HiddenCardsTakenEvent():
            return take_hidden_cards(game)
        case DeclarerGaveUpEvent():
            return game
        case CardsPassedEvent(card_to_next_seat=card_to_next_seat, card_to_prev_seat=card_to_prev_seat):
            return pass_cards(game, card_to_next_seat, card_to_prev_seat)
        case CardPlayedEvent(card=card):
            return play_card(game, card)
        case MarriagePointsAddedEvent(points=points, added_to=added_to):
            return add_marriage_points(game, points, added_to)
        case TrickTakenEvent(taken_by=taken_by):
            return take_trick(game, taken_by)
        case RoundFinishedEvent():
            return finish_round(game)
        case GameFinishedEvent():
            return finish_game(game)
