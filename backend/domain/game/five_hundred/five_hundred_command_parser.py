from typing import Any

from backend.domain.game.common.game_command import GameCommand

from .domain.five_hundred_card import FiveHundredCard
from .domain.five_hundred_command import MakeBidCommand, PassCardsCommand, PlayCardCommand


class FiveHundredCommandParser:
    def from_dict(self, raw_command: dict[str, Any]) -> GameCommand:
        match raw_command["type"]:
            case "make_bid":
                if "bid" not in raw_command:
                    raise ValueError(
                        f"Could not create five hundred command from json data, missing bid: {raw_command}"
                    )
                bid = int(raw_command["bid"])
                return MakeBidCommand(bid=bid)
            case "pass_cards":
                if "card_to_next_seat" not in raw_command or "card_to_prev_seat" not in raw_command:
                    raise ValueError(
                        f"Could not create five hundred command from json data, missing card_to_next_seat or card_to_prev_seat: {raw_command}"
                    )
                card_to_next_seat = FiveHundredCard.from_string(str(raw_command["card_to_next_seat"]))
                card_to_prev_seat = FiveHundredCard.from_string(str(raw_command["card_to_prev_seat"]))
                return PassCardsCommand(
                    card_to_next_seat=card_to_next_seat,
                    card_to_prev_seat=card_to_prev_seat,
                )
            case "play_card":
                if "card" not in raw_command:
                    raise ValueError(
                        f"Could not create five hundred command from json data, missing card: {raw_command}"
                    )
                card = FiveHundredCard.from_string(str(raw_command["card"]))
                return PlayCardCommand(card=card)
            case _:
                raise ValueError(f"Could not create five hundred command from json data, missing type: {raw_command}")
