import random
from typing import Any
from backend.games.five_hundred.domain.five_hundred_event import FiveHundredEvent
from backend.games.five_hundred.domain.five_hundred_game import FiveHundredGame
from backend.games.five_hundred.domain.five_hundred_seat import FiveHundredSeat
from backend.multiplayer.game_table import GameTable
from backend.core.game_config import GameTableConfig
from backend.games.five_hundred.five_hundred_game_engine import FiveHundredGameEngine
from backend.games.five_hundred.domain.five_hundred_command import (
    FiveHundredCommand,
    MakeBidCommand,
    PassCardsCommand,
    PlayCardCommand,
)
from backend.games.five_hundred.domain.five_hundred_phase import FiveHundredPhase
from backend.games.five_hundred.domain.constants import MIN_BID, MAX_BID, BID_STEP


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


def auto_player(
    table: GameTable[FiveHundredGame, FiveHundredCommand, FiveHundredEvent, FiveHundredSeat],
) -> list[FiveHundredEvent]:

    # Helper to find the user_id for the active seat
    def active_user_id(game_state: FiveHundredGame) -> str:
        active_seat = game_state.active_seat
        for uid, seat in table.players.items():
            if seat == active_seat:
                return uid
        return "none"

    all_events: list[FiveHundredEvent] = []

    # safety net to prevent infinite loop if game has a bug or something
    max_iterations_with_no_events = 100
    iterations = 0

    while True:

        game_state = table.game_state
        phase = game_state.round.phase

        if iterations >= max_iterations_with_no_events:
            print(f"Game state: {game_state}")
            print("Reached max iterations with no events")
            break
        iterations += 1

        active_uid = active_user_id(game_state)

        match phase:
            case FiveHundredPhase.BIDDING:
                highest_bid = game_state.round.highest_bid[1] if game_state.round.highest_bid else MIN_BID
                passing_probability = (
                    highest_bid / MAX_BID + 0.2
                )  # make passing probability a bit higher than just based on highest bid

                try:
                    if random.random() < passing_probability:
                        cmd = MakeBidCommand(bid=-1)
                    else:
                        cmd = MakeBidCommand(bid=random.choice(range(highest_bid, 120 + 1, BID_STEP)))

                    events = table.process_command(active_uid, cmd)

                    all_events.extend(events)
                    iterations = 0

                except ValueError as e:
                    print(f"Error during {phase} for user {active_uid} in seat {game_state.active_seat}: {e}")
                    continue

            case FiveHundredPhase.FORMING_HANDS:
                active_seats_cards = list(game_state.round.active_seats_info.hand.cards)

                try:
                    card1, card2 = random.sample(active_seats_cards, 2)
                    cmd = PassCardsCommand(card_to_next_seat=card1, card_to_prev_seat=card2)

                    events = table.process_command(active_uid, cmd)

                    all_events.extend(events)
                    iterations = 0

                except ValueError as e:
                    print(f"Error during {phase} for user {active_uid} in seat {game_state.active_seat}: {e}")
                    continue

            case FiveHundredPhase.PLAYING_CARDS:

                cards_allowed_to_play = game_state.round.active_seats_info.cards_allowed_to_play(
                    game_state.round.required_suit, game_state.round.trump_suit
                )

                try:
                    card_to_play = random.choice(cards_allowed_to_play)
                    cmd = PlayCardCommand(card=card_to_play)

                    events = table.process_command(active_uid, cmd)

                    all_events.extend(events)
                    iterations = 0

                except ValueError as e:
                    print(f"Error during {phase} for user {active_uid} in seat {game_state.active_seat}: {e}")
                    continue

            case FiveHundredPhase.GAME_FINISHED:
                print(f"Game state: {game_state}")
                break

    return all_events


# Example: run the auto player to completion and print the number of events
events = auto_player(fivehundred_table_1)
print(f"Auto play produced {len(events)} events")
