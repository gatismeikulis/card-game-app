from typing import Literal, TypedDict

from .five_hundred_card import FiveHundredCard
from .five_hundred_seat import FiveHundredSeat


class BidMadeEvent(TypedDict):
    type: Literal["BID_MADE"]
    bid: int
    made_by: FiveHundredSeat


class BiddingFinishedEvent(TypedDict):
    type: Literal["BIDDING_FINISHED"]


class HiddenCardsTakenEvent(TypedDict):
    type: Literal["HIDDEN_CARDS_TAKEN"]


class CardsPassedEvent(TypedDict):
    type: Literal["CARDS_PASSED"]
    card_to_next_seat: FiveHundredCard
    card_to_prev_seat: FiveHundredCard


class CardPlayedEvent(TypedDict):
    type: Literal["CARD_PLAYED"]
    card: FiveHundredCard
    played_by: FiveHundredSeat


class MarriagePointsAddedEvent(TypedDict):
    type: Literal["MARRIAGE_POINTS_ADDED"]
    points: int
    added_to: FiveHundredSeat


class TrickTakenEvent(TypedDict):
    type: Literal["TRICK_TAKEN"]
    taken_by: FiveHundredSeat


class RoundFinishedEvent(TypedDict):
    type: Literal["ROUND_FINISHED"]


class GameFinishedEvent(TypedDict):
    type: Literal["GAME_FINISHED"]


FiveHundredEvent = (
    BidMadeEvent
    | BiddingFinishedEvent
    | HiddenCardsTakenEvent
    | CardsPassedEvent
    | CardPlayedEvent
    | RoundFinishedEvent
    | GameFinishedEvent
    | MarriagePointsAddedEvent
    | TrickTakenEvent
)
