from dataclasses import replace
from ..domain.five_hundred_event import (
    DeckShuffledEvent,
    BiddingFinishedEvent,
    BidMadeEvent,
    CardPlayedEvent,
    CardsPassedEvent,
    FiveHundredEvent,
    GameEndedEvent,
    DeclarerGaveUpEvent,
    HiddenCardsTakenEvent,
    MarriagePointsAddedEvent,
    RoundFinishedEvent,
    TrickTakenEvent,
)
from ..domain.five_hundred_game import FiveHundredGame
from ..logic.add_marriage_points import add_marriage_points
from ..logic.deal_cards import deal_cards
from ..logic.give_up import give_up
from ..logic.finish_bidding import finish_bidding
from ..logic.end_game import end_game
from ..logic.finish_round import finish_round
from ..logic.make_bid import make_bid
from ..logic.pass_cards import pass_cards
from ..logic.play_card import play_card
from ..logic.take_hidden_cards import take_hidden_cards
from ..logic.take_trick import take_trick


def apply_event(game: FiveHundredGame, event: FiveHundredEvent) -> FiveHundredGame:
    game_updated = replace(game, event_number=event.seq_number)
    match event:
        case DeckShuffledEvent(deck=deck):
            return deal_cards(game_updated, deck)
        case BidMadeEvent(bid=bid):
            return make_bid(game_updated, bid)
        case BiddingFinishedEvent():
            return finish_bidding(game_updated)
        case HiddenCardsTakenEvent():
            return take_hidden_cards(game_updated)
        case DeclarerGaveUpEvent():
            return give_up(game_updated)
        case CardsPassedEvent(card_to_next_seat=card_to_next_seat, card_to_prev_seat=card_to_prev_seat):
            return pass_cards(game_updated, card_to_next_seat, card_to_prev_seat)
        case CardPlayedEvent(card=card):
            return play_card(game_updated, card)
        case MarriagePointsAddedEvent(points=points, added_to=added_to):
            return add_marriage_points(game_updated, points, added_to)
        case TrickTakenEvent(taken_by=taken_by):
            return take_trick(game_updated, taken_by)
        case RoundFinishedEvent(points=points):
            return finish_round(game_updated, points_per_seat=points)
        case GameEndedEvent(reason=reason, seat=seat):
            return end_game(game_updated, reason=reason, blamed_seat=seat)
