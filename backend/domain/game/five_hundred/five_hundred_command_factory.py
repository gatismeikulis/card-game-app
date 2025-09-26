from typing import Any

from .domain.five_hundred_card import FiveHundredCard
from .domain.five_hundred_command import FiveHundredCommand, MakeBidCommand, PassCardsCommand, PlayCardCommand


class FiveHundredCommandFactory:
    @staticmethod
    def from_json(data: dict[str, Any]) -> FiveHundredCommand:
        match data["type"]:
            case "bid":
                if "bid" not in data:
                    raise ValueError("Could not create five hundred command from json data")
                return MakeBidCommand(bid=data["bid"])
            case "pass_cards":
                if "card_to_next_seat" not in data or "card_to_prev_seat" not in data:
                    raise ValueError("Could not create five hundred command from json data")
                card_to_next_seat = FiveHundredCard.from_string(data["card_to_next_seat"])
                card_to_prev_seat = FiveHundredCard.from_string(data["card_to_prev_seat"])
                return PassCardsCommand(
                    card_to_next_seat=card_to_next_seat,
                    card_to_prev_seat=card_to_prev_seat,
                )
            case "play_card":
                if "card" not in data:
                    raise ValueError("Could not create five hundred command from json data")
                card = FiveHundredCard.from_string(data["card"])
                return PlayCardCommand(card=card)
            case _:
                raise ValueError("Could not create five hundred command from json data")
