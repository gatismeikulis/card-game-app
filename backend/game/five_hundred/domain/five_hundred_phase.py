from enum import Enum
from typing import override


class FiveHundredPhase(Enum):
    INITIALIZING = "Initializing"
    BIDDING = "Bidding"
    FORMING_HANDS = "Forming Hands"
    PLAYING_CARDS = "Playing Cards"
    GAME_FINISHED = "Game Ended"

    @override
    def __str__(self) -> str:
        return f"{self.value} phase"

    @override
    def __repr__(self) -> str:
        return self.__str__()
