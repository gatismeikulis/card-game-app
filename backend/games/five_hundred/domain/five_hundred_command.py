from typing import Literal, TypedDict

from .five_hundred_card import FiveHundredCard


class MakeBidCommand(TypedDict):
    type: Literal["MAKE_BID"]
    bid: int


class PassCardsCommand(TypedDict):
    type: Literal["PASS_CARDS"]
    card_to_next_seat: FiveHundredCard
    card_to_prev_seat: FiveHundredCard


class PlayCardCommand(TypedDict):
    type: Literal["PLAY_CARD"]
    card: FiveHundredCard


FiveHundredCommand = MakeBidCommand | PassCardsCommand | PlayCardCommand
