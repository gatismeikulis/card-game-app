import random
from typing import Any
from backend.games.five_hundred.domain.five_hundred_event import FiveHundredEvent
from backend.games.five_hundred.domain.five_hundred_game import FiveHundredGame
from backend.games.five_hundred.domain.five_hundred_seat import FiveHundredSeat
from backend.multiplayer.game_table import GameTable
from backend.core.game_config import GameTableConfig
from backend.games.five_hundred.five_hundred_game_engine import FiveHundredGameEngine
from backend.games.five_hundred.domain.five_hundred_command import FiveHundredCommand, MakeBidCommand, PassCardsCommand


tables: list[GameTable[Any, Any, Any, Any]] = []

fivehundred_table_1 = GameTable[FiveHundredGame, FiveHundredCommand, FiveHundredEvent, FiveHundredSeat](
    table_id="fivehundred_table_1",
    config=GameTableConfig(min_players=3, max_players=3, automatic_start=True),
    engine=FiveHundredGameEngine(),
)

fivehundred_table_1.add_player(user_id="user_1", seat=FiveHundredSeat(1))
fivehundred_table_1.add_player(user_id="user_2", seat=FiveHundredSeat(2))
fivehundred_table_1.add_player(user_id="user_3", seat=FiveHundredSeat(3))
fivehundred_table_1.start_game()
print(fivehundred_table_1)
events = fivehundred_table_1.process_command("user_1", MakeBidCommand(bid=100))
print(events)
events = fivehundred_table_1.process_command("user_2", MakeBidCommand(bid=120))
print(events)
events = fivehundred_table_1.process_command("user_3", MakeBidCommand(bid=-1))
print(events)
events = fivehundred_table_1.process_command("user_1", MakeBidCommand(bid=-1))
print(events)
events = fivehundred_table_1.process_command("user_2", MakeBidCommand(bid=160))
print(events)
# pass 2 random cards
cards = list(fivehundred_table_1.game_state.round.active_seats_info.hand.cards)
card1 = cards[0]
card2 = cards[1]
events = fivehundred_table_1.process_command(
    "user_2", PassCardsCommand(card_to_next_seat=card1, card_to_prev_seat=card2)
)
print(events)

print(fivehundred_table_1)
