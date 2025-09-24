from dataclasses import dataclass
from typing import ClassVar, Literal

from backend.games.common.command import Command

from .five_hundred_card import FiveHundredCard


@dataclass(frozen=True, slots=True)
class MakeBidCommand(Command):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["make_bid"]] = "make_bid"
    bid: int


@dataclass(frozen=True, slots=True)
class PassCardsCommand(Command):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["pass_cards"]] = "pass_cards"
    card_to_next_seat: FiveHundredCard
    card_to_prev_seat: FiveHundredCard


@dataclass(frozen=True, slots=True)
class PlayCardCommand(Command):
    source: ClassVar[Literal["five_hundred"]] = "five_hundred"
    type: ClassVar[Literal["play_card"]] = "play_card"
    card: FiveHundredCard


FiveHundredCommand = MakeBidCommand | PassCardsCommand | PlayCardCommand
