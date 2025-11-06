from typing import Any, override

from ..common.game_exception import GameParsingException
from ..common.game_event import GameEvent
from ..common.game_event_parser import GameEventParser
from .domain.five_hundred_event import (
    BidMadeEvent,
    BiddingFinishedEvent,
    DeckShuffledEvent,
    HiddenCardsTakenEvent,
    CardsPassedEvent,
    CardPlayedEvent,
    MarriagePointsAddedEvent,
    TrickTakenEvent,
    RoundFinishedEvent,
    GameEndedEvent,
)


class FiveHundredEventParser(GameEventParser):
    @override
    def from_dict(self, data: dict[str, Any]) -> GameEvent:
        event_type = data["type"]

        match event_type:
            case "deck_shuffled":
                return DeckShuffledEvent.from_dict(data)
            case "bid_made":
                return BidMadeEvent.from_dict(data)
            case "bidding_finished":
                return BiddingFinishedEvent.from_dict(data)
            case "hidden_cards_taken":
                return HiddenCardsTakenEvent.from_dict(data)
            case "cards_passed":
                return CardsPassedEvent.from_dict(data)
            case "card_played":
                return CardPlayedEvent.from_dict(data)
            case "marriage_points_added":
                return MarriagePointsAddedEvent.from_dict(data)
            case "trick_taken":
                return TrickTakenEvent.from_dict(data)
            case "round_finished":
                return RoundFinishedEvent.from_dict(data)
            case "game_ended":
                return GameEndedEvent.from_dict(data)
            case _:
                raise GameParsingException(
                    reason="game_event_parsing_error",
                    detail=f"Could not parse five hundred game event from input: {data}",
                )
