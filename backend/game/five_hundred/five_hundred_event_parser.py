from typing import Any

from ..common.game_event import GameEvent
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
    GameFinishedEvent,
)


class FiveHundredEventParser:
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
            case "game_finished":
                return GameFinishedEvent.from_dict(data)
            case _:
                raise ValueError(f"Unknown event type: {event_type}")
