from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar, Literal

from ...common.game_event import GameEvent
from .five_hundred_card import FiveHundredCard
from .five_hundred_seat import FiveHundredSeat


@dataclass(frozen=True, slots=True)
class BidMadeEvent(GameEvent):
    type: ClassVar[Literal["bid_made"]] = "bid_made"
    bid: int
    made_by: FiveHundredSeat


@dataclass(frozen=True, slots=True)
class BiddingFinishedEvent(GameEvent):
    type: ClassVar[Literal["bidding_finished"]] = "bidding_finished"


@dataclass(frozen=True, slots=True)
class HiddenCardsTakenEvent(GameEvent):
    type: ClassVar[Literal["hidden_cards_taken"]] = "hidden_cards_taken"


@dataclass(frozen=True, slots=True)
class CardsPassedEvent(GameEvent):
    type: ClassVar[Literal["cards_passed"]] = "cards_passed"
    card_to_next_seat: FiveHundredCard
    card_to_prev_seat: FiveHundredCard


@dataclass(frozen=True, slots=True)
class CardPlayedEvent(GameEvent):
    type: ClassVar[Literal["card_played"]] = "card_played"
    card: FiveHundredCard
    played_by: FiveHundredSeat


@dataclass(frozen=True, slots=True)
class MarriagePointsAddedEvent(GameEvent):
    type: ClassVar[Literal["marriage_points_added"]] = "marriage_points_added"
    points: int
    added_to: FiveHundredSeat


@dataclass(frozen=True, slots=True)
class TrickTakenEvent(GameEvent):
    type: ClassVar[Literal["trick_taken"]] = "trick_taken"
    taken_by: FiveHundredSeat
    cards: Sequence[FiveHundredCard]


@dataclass(frozen=True, slots=True)
class RoundFinishedEvent(GameEvent):
    type: ClassVar[Literal["round_finished"]] = "round_finished"
    round_number: int


@dataclass(frozen=True, slots=True)
class GameFinishedEvent(GameEvent):
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
