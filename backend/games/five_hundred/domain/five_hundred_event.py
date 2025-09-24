from dataclasses import dataclass
from typing import ClassVar, Literal

from backend.games.common.event import Event

from .five_hundred_card import FiveHundredCard
from .five_hundred_seat import FiveHundredSeat


@dataclass(frozen=True, slots=True)
class BidMadeEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["bid_made"]] = "bid_made"
    bid: int
    made_by: FiveHundredSeat


@dataclass(frozen=True, slots=True)
class BiddingFinishedEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["bidding_finished"]] = "bidding_finished"


@dataclass(frozen=True, slots=True)
class HiddenCardsTakenEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["hidden_cards_taken"]] = "hidden_cards_taken"


@dataclass(frozen=True, slots=True)
class CardsPassedEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["cards_passed"]] = "cards_passed"
    card_to_next_seat: FiveHundredCard
    card_to_prev_seat: FiveHundredCard


@dataclass(frozen=True, slots=True)
class CardPlayedEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["card_played"]] = "card_played"
    card: FiveHundredCard
    played_by: FiveHundredSeat


@dataclass(frozen=True, slots=True)
class MarriagePointsAddedEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["marriage_points_added"]] = "marriage_points_added"
    points: int
    added_to: FiveHundredSeat


@dataclass(frozen=True, slots=True)
class TrickTakenEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["trick_taken"]] = "trick_taken"
    taken_by: FiveHundredSeat


@dataclass(frozen=True, slots=True)
class RoundFinishedEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["round_finished"]] = "round_finished"


@dataclass(frozen=True, slots=True)
class GameFinishedEvent(Event):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["game_finished"]] = "game_finished"


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
