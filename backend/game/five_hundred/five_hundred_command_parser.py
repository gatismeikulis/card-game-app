from typing import Any, override

from ..common.game_exception import GameParsingException
from ..common.game_command import GameCommand
from ..common.game_command_parser import GameCommandParser
from .domain.five_hundred_card import FiveHundredCard
from .domain.five_hundred_command import (
    MakeBidCommand,
    PassCardsCommand,
    PlayCardCommand,
)


class FiveHundredCommandParser(GameCommandParser):
    @override
    def from_dict(self, raw_command: dict[str, Any]) -> GameCommand:
        def error(type: str = "") -> GameParsingException:
            return GameParsingException(
                reason="command_parsing_error", detail=f"Could not create '{type}' command from input: {raw_command}"
            )

        match raw_command["type"]:
            case "make_bid":
                try:
                    bid = int(raw_command["params"]["bid"])
                except Exception:
                    raise error("make_bid")
                return MakeBidCommand(bid=bid)
            case "pass_cards":
                try:
                    card_to_next_seat = FiveHundredCard.from_string(raw_command["params"]["card_to_next_seat"])
                    card_to_prev_seat = FiveHundredCard.from_string(raw_command["params"]["card_to_prev_seat"])
                except Exception:
                    raise error("pass_cards")
                return PassCardsCommand(
                    card_to_next_seat=card_to_next_seat,
                    card_to_prev_seat=card_to_prev_seat,
                )
            case "play_card":
                try:
                    card = FiveHundredCard.from_string(raw_command["params"]["card"])
                except Exception:
                    raise error("play_card")
                return PlayCardCommand(card=card)
            case _:
                raise error()
