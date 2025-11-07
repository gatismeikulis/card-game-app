from dataclasses import dataclass
from typing import ClassVar, Literal

from ...common.game_ending import GameEndingReason
from ...common.seat import Seat
from ...common.game_command import GameCommand
from .five_hundred_card import FiveHundredCard


@dataclass(frozen=True, slots=True)
class StartGameCommand(GameCommand):
    type: ClassVar[Literal["start_game"]] = "start_game"


@dataclass(frozen=True, slots=True)
class MakeBidCommand(GameCommand):
    type: ClassVar[Literal["make_bid"]] = "make_bid"
    bid: int


@dataclass(frozen=True, slots=True)
class GiveUpCommand(GameCommand):
    type: ClassVar[Literal["give_up"]] = "give_up"


@dataclass(frozen=True, slots=True)
class PassCardsCommand(GameCommand):
    type: ClassVar[Literal["pass_cards"]] = "pass_cards"
    card_to_next_seat: FiveHundredCard
    card_to_prev_seat: FiveHundredCard


@dataclass(frozen=True, slots=True)
class PlayCardCommand(GameCommand):
    type: ClassVar[Literal["play_card"]] = "play_card"
    card: FiveHundredCard


@dataclass(frozen=True, slots=True)
class EndGameCommand(GameCommand):
    type: ClassVar[Literal["end_game"]] = "end_game"
    reason: GameEndingReason  # cancel/abort
    seat: Seat | None = None  # when abort, then seat to blame


FiveHundredCommand = (
    StartGameCommand | MakeBidCommand | GiveUpCommand | PassCardsCommand | PlayCardCommand | EndGameCommand
)
