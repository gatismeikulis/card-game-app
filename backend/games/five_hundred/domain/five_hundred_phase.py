from enum import Enum
from typing import override


class FiveHundredPhase(Enum):
    BIDDING = "Bidding"
    FORMING_HANDS = "Forming Hands"
    PLAYING_CARDS = "Playing Cards"
    FINISHING_ROUND = "Finishing Round"
    GAME_FINISHED = "Game Ended"

    @override
    def __str__(self) -> str:
        return self.value.upper()

    @override
    def __repr__(self) -> str:
        return self.__str__()
