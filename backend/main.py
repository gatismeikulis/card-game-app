from backend.application.bot_strategy_registry import BotStrategyRegistry
from backend.application.game_command_parsing_service import GameCommandParsingService
from backend.application.game_table_manager import GameTableManager
from backend.domain.core.user_id import UserId
from backend.domain.game.bot_strategy_kind import BotStrategyKind
from backend.domain.game.game_name import GameName
from backend.domain.lobby.lobby import Lobby
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.game_table_factory import GameTableFactory

fivehundred_table_1 = GameTableFactory.create(
    config=GameTableConfig(
        game_name=GameName.FIVE_HUNDRED,
        min_players=3,
        max_players=3,
    ),
)

user_id_1 = UserId.generate()

fivehundred_table_1.add_player(user_id=user_id_1)
fivehundred_table_1.add_player(user_id=UserId.generate())
fivehundred_table_1.add_player(user_id=UserId.generate())
fivehundred_table_1.start_game(user_id_1)


# def auto_player(
#     table: GameTable,
# ) -> list[GameEvent]:

#     # Helper to find the user_id for the active seat
#     def active_user_id(game_state: FiveHundredGame) -> UserId:
#         active_seat = game_state.active_seat
#         for user_id, player in table.players.items():
#             if player.seat_number == active_seat.number:
#                 return user_id
#         return UserId.generate()  # should not happen

#     all_events: list[FiveHundredEvent] = []

#     # safety net to prevent infinite loop if game has a bug or something
#     max_iterations_with_no_events = 100
#     iterations = 0

#     while True:

#         game_state = table.game_state
#         phase = game_state.round.phase

#         if iterations >= max_iterations_with_no_events:
#             print(f"Game state: {game_state}")
#             print("Reached max iterations with no events")
#             break
#         iterations += 1

#         active_uid = active_user_id(game_state)

#         match phase:
#             case FiveHundredPhase.BIDDING:
#                 highest_bid = game_state.round.highest_bid[1] if game_state.round.highest_bid else MIN_BID
#                 passing_probability = (
#                     highest_bid / MAX_BID + 0.2
#                 )  # make passing probability a bit higher than just based on highest bid

#                 try:
#                     if random.random() < passing_probability:
#                         cmd: FiveHundredCommand = MakeBidCommand(bid=-1)
#                     else:
#                         cmd = MakeBidCommand(bid=random.choice(range(highest_bid, 120 + 1, BID_STEP)))

#                     events = table.take_turn(active_uid, cmd)

#                     all_events.extend(events)
#                     iterations = 0

#                 except ValueError as e:
#                     print(f"Error during {phase} for user {active_uid} in seat {game_state.active_seat}: {e}")
#                     continue

#             case FiveHundredPhase.FORMING_HANDS:
#                 active_seats_cards = list(game_state.active_seats_info.hand.cards)

#                 try:
#                     card1, card2 = random.sample(active_seats_cards, 2)
#                     cmd = PassCardsCommand(card_to_next_seat=card1, card_to_prev_seat=card2)

#                     events = table.take_turn(active_uid, cmd)

#                     all_events.extend(events)
#                     iterations = 0

#                 except ValueError as e:
#                     print(f"Error during {phase} for user {active_uid} in seat {game_state.active_seat}: {e}")
#                     continue

#             case FiveHundredPhase.PLAYING_CARDS:

#                 cards_allowed_to_play = game_state.active_seats_info.cards_allowed_to_play(
#                     game_state.round.required_suit, game_state.round.trump_suit
#                 )

#                 try:
#                     card_to_play = random.choice(cards_allowed_to_play)
#                     cmd = PlayCardCommand(card=card_to_play)

#                     events = table.take_turn(active_uid, cmd)

#                     all_events.extend(events)
#                     iterations = 0

#                 except ValueError as e:
#                     print(f"Error during {phase} for user {active_uid} in seat {game_state.active_seat}: {e}")
#                     continue

#             case FiveHundredPhase.GAME_FINISHED:
#                 print(f"Game state: {game_state}")
#                 break

#     return all_events


# Example: run the auto player to completion and print the number of events
# events = auto_player(fivehundred_table_1)
# print(f"Auto play produced {len(events)} events")


game_command_parsing_service = GameCommandParsingService()
bot_strategy_registry = BotStrategyRegistry()
lobby = Lobby()
game_table_manager = GameTableManager(lobby, game_command_parsing_service, bot_strategy_registry)

game_table_manager.add_table(
    GameTableConfig(
        game_name=GameName.FIVE_HUNDRED,
        min_players=3,
        max_players=3,
    ),
)

tables = game_table_manager.get_tables()

table_id = tables[0].id

user_id_1 = UserId.generate()
user_id_2 = UserId.generate()
user_id_3 = UserId.generate()


game_table_manager.join_table(table_id, user_id_1, preferred_seat_number=1)
game_table_manager.add_bot_player(
    table_id, user_id_2, bot_strategy_kind=BotStrategyKind.RANDOM, preferred_seat_number=2
)
game_table_manager.add_bot_player(
    table_id, user_id_3, bot_strategy_kind=BotStrategyKind.RANDOM, preferred_seat_number=3
)
print(game_table_manager.get_tables()[0])
game_table_manager.start_game(table_id, user_id_1)
print(game_table_manager.get_tables()[0])


print(game_table_manager.take_regular_turn(table_id, user_id_1, {"type": "make_bid", "bid": 100}))
print(game_table_manager.get_tables()[0])
print(game_table_manager.take_automatic_turn(table_id, user_id_2))
print(game_table_manager.get_tables()[0])
