from .application.apply_event import apply_event
from .application.handle_command import handle_command
from .domain.constants import (
    EMPTY_HAND_SIZE,
    LARGE_MARRIAGE_POINTS,
    SMALL_MARRIAGE_POINTS,
)
from .domain.five_hundred_command import FiveHundredCommand
from .domain.five_hundred_event import (
    BiddingFinishedEvent,
    GameFinishedEvent,
    FiveHundredEvent,
    HiddenCardsTakenEvent,
    MarriagePointsAddedEvent,
    RoundFinishedEvent,
    TrickTakenEvent,
)
from .domain.five_hundred_game import FiveHundredGame
from .engine.helpers import (
    get_next_seat_to_bid,
    get_trick_winning_card,
    is_played_card_part_of_marriage,
)


# Entry point for the game
def process_command(
    game: FiveHundredGame, command: FiveHundredCommand
) -> tuple[FiveHundredGame, list[FiveHundredEvent]]:

    event = handle_command(game, command)

    game_updated = game
    all_events: list[FiveHundredEvent] = []

    current_event = event

    while current_event is not None:
        game_updated = apply_event(game_updated, current_event)
        all_events.append(current_event)

        current_event = check_for_additional_events(game_updated, current_event)

    return game_updated, all_events


def check_for_additional_events(game: FiveHundredGame, last_event: FiveHundredEvent) -> FiveHundredEvent | None:

    if last_event["type"] == "BID_MADE":
        current_highest_bidder = game.round.highest_bid[0] if game.round.highest_bid else None
        next_seat_to_bid = get_next_seat_to_bid(game.round.active_seat, game.round.seat_infos)
        have_all_seats_passed = all(seat_info.bid < 0 for seat_info in game.round.seat_infos.values())
        is_current_bidder_the_highest_bidder = current_highest_bidder == last_event["made_by"]
        if (is_current_bidder_the_highest_bidder and next_seat_to_bid is None) or have_all_seats_passed:
            return BiddingFinishedEvent(type="BIDDING_FINISHED")

    elif last_event["type"] == "BIDDING_FINISHED":
        if game.round.highest_bid is None:
            return RoundFinishedEvent(type="ROUND_FINISHED")
        else:
            return HiddenCardsTakenEvent(type="HIDDEN_CARDS_TAKEN")

    elif last_event["type"] == "CARD_PLAYED":
        cards_on_board_count = game.round.cards_on_board_count
        played_card = last_event["card"]
        card_played_by = last_event["played_by"]

        # if 1st card played, check for marriage.
        if cards_on_board_count == 1:
            cards_left_in_hand = game.round.seat_infos[card_played_by].hand.cards
            marriage_possible = is_played_card_part_of_marriage(played_card, cards_left_in_hand)

            if not marriage_possible:
                return None
            else:
                if played_card.suit == game.round.trump_suit:
                    return MarriagePointsAddedEvent(
                        type="MARRIAGE_POINTS_ADDED",
                        points=LARGE_MARRIAGE_POINTS,
                        added_to=card_played_by,
                    )
                elif played_card.suit != game.round.trump_suit and game.round.is_marriage_announced:
                    return MarriagePointsAddedEvent(
                        type="MARRIAGE_POINTS_ADDED",
                        points=SMALL_MARRIAGE_POINTS,
                        added_to=card_played_by,
                    )

        # if 3rd card played for this trick, then trick is finished
        elif cards_on_board_count == 3:
            cards_on_board = game.round.cards_on_board
            trick_cards = [card for card in cards_on_board.values() if card is not None]
            trick_winning_card = get_trick_winning_card(trick_cards, game.round.required_suit, game.round.trump_suit)
            trick_winning_seat = next(seat for seat, card in cards_on_board.items() if card == trick_winning_card)
            return TrickTakenEvent(type="TRICK_TAKEN", taken_by=trick_winning_seat)

    elif last_event["type"] == "TRICK_TAKEN":
        # if any of seats does not have cards left, then round is finished
        if len(game.round.active_seats_info.hand.cards) == EMPTY_HAND_SIZE:
            return RoundFinishedEvent(type="ROUND_FINISHED")

    elif last_event["type"] == "ROUND_FINISHED":
        if any(points <= 0 for points in game.summary.values()):
            return GameFinishedEvent(type="GAME_FINISHED")
        return None
