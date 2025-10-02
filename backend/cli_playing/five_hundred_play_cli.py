import time
from collections.abc import Sequence

from backend.domain.core.user_id import UserId
from backend.domain.game.common.game_command import GameCommand
from backend.domain.game.common.game_event import GameEvent
from backend.domain.game.five_hundred.domain.constants import BID_STEP, LARGE_MARRIAGE_POINTS, MAX_BID, MIN_BID
from backend.domain.game.five_hundred.domain.five_hundred_card import FiveHundredCard
from backend.domain.game.five_hundred.domain.five_hundred_command import (
    MakeBidCommand,
    PassCardsCommand,
    PlayCardCommand,
)
from backend.domain.game.five_hundred.domain.five_hundred_event import (
    BiddingFinishedEvent,
    BidMadeEvent,
    CardPlayedEvent,
    CardsPassedEvent,
    FiveHundredEvent,
    GameFinishedEvent,
    MarriagePointsAddedEvent,
    RoundFinishedEvent,
    TrickTakenEvent,
)
from backend.domain.game.five_hundred.domain.five_hundred_game import FiveHundredGame
from backend.domain.game.five_hundred.domain.five_hundred_phase import FiveHundredPhase
from backend.domain.game.five_hundred.five_hundred_random_bot_strategy import FiveHundredRandomBotStrategy
from backend.domain.game.game_name import GameName
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.game_table_factory import GameTableFactory


def five_hundred_play_cli(delay_between_events: float = -1) -> list[GameEvent]:

    table = GameTableFactory.create(
        config=GameTableConfig(
            game_name=GameName.FIVE_HUNDRED,
            min_players=3,
            max_players=3,
        ),
    )

    user_id_1 = UserId.generate()
    user_id_2 = UserId.generate()
    user_id_3 = UserId.generate()

    table.add_player(user_id=user_id_1, preferred_seat_number=1)
    table.add_player(user_id=user_id_2, preferred_seat_number=2, bot_strategy=FiveHundredRandomBotStrategy())
    table.add_player(user_id=user_id_3, preferred_seat_number=3, bot_strategy=FiveHundredRandomBotStrategy())

    table.start_game(user_id_1)

    print(table)

    all_events: list[GameEvent] = []
    events: Sequence[GameEvent] = []

    def print_logs(events: Sequence[GameEvent], game_state: FiveHundredGame) -> None:
        for event in events:
            if not isinstance(event, FiveHundredEvent):
                continue
            if delay_between_events > 0:
                time.sleep(delay_between_events)
            match event:
                case BidMadeEvent(bid=bid, made_by=made_by):
                    print(f"Player {made_by} {f"bid {bid}" if bid >= 0 else 'passed'}")
                case BiddingFinishedEvent():
                    highest_bid = game_state.round.highest_bid
                    print(
                        f"Bidding finished, highest bid is {highest_bid[1] if highest_bid else 'unknown'} by player {highest_bid[0] if highest_bid else 'unknown'}"
                    )
                case CardsPassedEvent():
                    print(f"Player {game_state.active_seat} finished forming hands and is starting to play cards")
                case CardPlayedEvent(card=card, played_by=played_by):
                    print(f"Player {played_by} played {card}")
                case MarriagePointsAddedEvent(points=points, added_to=added_to):
                    print(
                        f"Player {added_to} announced {"large" if points == LARGE_MARRIAGE_POINTS else "small"} marriage"
                    )
                case TrickTakenEvent(taken_by=taken_by, cards=cards):
                    print(f"Trick completed, cards: {cards} taken by player {taken_by}")
                case RoundFinishedEvent(round_number=round_number):
                    print(f"\nRound {round_number} finished")
                    print(f"Current scores: {game_state.summary}")
                    print(f"Next round will be started by player {game_state.round.first_seat}")
                case GameFinishedEvent():
                    print("Game finished")
                    print(f"Final scores: {game_state.summary}")
                    print(f"Winners: {game_state.winners}")
                case _:
                    continue

    def extract_card_from_input(cards: Sequence[FiveHundredCard], card_str_or_index: str) -> FiveHundredCard:
        if card_str_or_index.isdigit():
            index = int(card_str_or_index)
            return cards[index - 1]
        else:
            card = next(
                (c for c in cards if c == FiveHundredCard.from_string(card_str_or_index)),
                None,
            )
            if card is None:
                raise ValueError("Card not found in hand")
            return card

    while True:
        game_state = table.game_state
        if not isinstance(game_state, FiveHundredGame):
            raise TypeError(f"five_hundred_play_cli expects FiveHundredGame, got {type(game_state).__name__}")

        active_user_id = table.active_user_id
        active_player = table.players[active_user_id]

        print_logs(events, game_state)

        events = []

        phase = game_state.round.phase

        if active_player.bot_strategy is not None and phase != FiveHundredPhase.GAME_FINISHED:
            events = table.take_automatic_turn(active_user_id)
            all_events.extend(events)
        else:
            match phase:
                case FiveHundredPhase.BIDDING:
                    print(
                        f"\nBidding phase. Your hand: {game_state.active_seats_info.hand} \nEnter bid amount ({game_state.round.highest_bid[1] + BID_STEP if game_state.round.highest_bid else MIN_BID} -> {MAX_BID}) with step of {BID_STEP} or negative number to pass:"
                    )
                    try:
                        bid = int(input("> "))
                        cmd: GameCommand = MakeBidCommand(bid=bid)
                        events = table.take_regular_turn(active_user_id, cmd)
                        all_events.extend(events)
                    except ValueError as e:
                        print(f"Invalid input: {str(e)}")
                        continue
                case FiveHundredPhase.FORMING_HANDS:
                    print(
                        f"\nForming hands phase. Your hand: {game_state.active_seats_info.hand} \nEnter two cards (eg. Ah Kd) or indexes (1 -> 10) of the cards to pass to other players:"
                    )
                    try:
                        card1_str, card2_str = input("> ").split()
                        cards = list(game_state.active_seats_info.hand.cards)

                        card1 = extract_card_from_input(cards, card1_str)
                        card2 = extract_card_from_input(cards, card2_str)

                        if card1 == card2:
                            raise ValueError("Cannot pass same card to both players")

                        cmd = PassCardsCommand(
                            card_to_next_seat=card1,
                            card_to_prev_seat=card2,
                        )
                        events = table.take_regular_turn(active_user_id, cmd)
                        all_events.extend(events)
                    except (ValueError, IndexError) as e:
                        print(f"Invalid input: {str(e)}")
                        continue
                case FiveHundredPhase.PLAYING_CARDS:
                    allowed_cards = game_state.active_seats_info.cards_allowed_to_play(
                        game_state.round.required_suit, game_state.round.trump_suit
                    )
                    print(
                        f"\nPlaying cards phase. Your hand: {game_state.active_seats_info.hand}, You are allowd to play: {" ".join(str(card) for card in allowed_cards)}\nEnter card (eg. Ah) or index (1 -> {len(allowed_cards)}) of the card to play:"
                    )
                    try:
                        card_str = input("> ")
                        card = extract_card_from_input(allowed_cards, card_str)
                        cmd = PlayCardCommand(card=card)
                        events = table.take_regular_turn(active_user_id, cmd)
                        all_events.extend(events)
                    except (ValueError, IndexError) as e:
                        print(f"Invalid input: {str(e)}")
                        continue
                case FiveHundredPhase.GAME_FINISHED:
                    return all_events


if __name__ == "__main__":
    five_hundred_play_cli()
