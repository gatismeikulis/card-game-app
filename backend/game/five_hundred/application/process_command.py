from collections.abc import Sequence

from ...common.game_ending import GameEndingReason
from ..domain.constants import (
    EMPTY_HAND_SIZE,
    LARGE_MARRIAGE_POINTS,
    NOT_ALLOWED_TO_BID_THRESHOLD,
    SMALL_MARRIAGE_POINTS,
)
from ..domain.five_hundred_deck import FiveHundredDeck
from ..domain.five_hundred_command import FiveHundredCommand
from ..domain.five_hundred_event import (
    BiddingFinishedEvent,
    BidMadeEvent,
    CardPlayedEvent,
    DeckShuffledEvent,
    FiveHundredEvent,
    GameEndedEvent,
    HiddenCardsTakenEvent,
    MarriagePointsAddedEvent,
    RoundFinishedEvent,
    TrickTakenEvent,
    DeclarerGaveUpEvent,
)
from ..domain.five_hundred_game import FiveHundredGame
from ..logic.helpers import get_next_seat_to_bid, get_trick_winning_card, is_played_card_part_of_marriage
from .apply_event import apply_event
from .handle_command import handle_command


def process_command(
    game: FiveHundredGame, command: FiveHundredCommand
) -> tuple[FiveHundredGame, Sequence[FiveHundredEvent]]:
    event = handle_command(game, command)

    game_updated = game
    all_events: list[FiveHundredEvent] = []

    current_event: FiveHundredEvent | None = event

    while current_event is not None:
        game_updated = apply_event(game_updated, current_event)
        all_events.append(current_event)

        current_event = check_for_additional_events(game_updated, current_event)

    return game_updated, all_events


def check_for_additional_events(game: FiveHundredGame, last_event: FiveHundredEvent) -> FiveHundredEvent | None:
    match last_event:
        case BidMadeEvent(made_by=made_by):
            current_highest_bidder = game.round.highest_bid[0] if game.round.highest_bid else None
            next_seat_to_bid = get_next_seat_to_bid(game.active_seat, game.round.seat_infos)
            have_all_seats_passed = all(seat_info.bid < 0 for seat_info in game.round.seat_infos.values())
            is_current_bidder_the_highest_bidder = current_highest_bidder == made_by
            if (is_current_bidder_the_highest_bidder and next_seat_to_bid is None) or have_all_seats_passed:
                return BiddingFinishedEvent(
                    bid=game.round.highest_bid[1] if game.round.highest_bid else None,
                    made_by=game.round.highest_bid[0] if game.round.highest_bid else None,
                )
            return None

        case BiddingFinishedEvent():
            if game.round.highest_bid is None:
                return RoundFinishedEvent(round_number=game.round.round_number, declarer=None, given_up=False)
            else:
                return HiddenCardsTakenEvent()

        case DeclarerGaveUpEvent():
            return RoundFinishedEvent(
                round_number=game.round.round_number,
                declarer=game.round.highest_bid[0] if game.round.highest_bid else None,
                given_up=True,
            )

        case CardPlayedEvent(played_by=card_played_by, card=played_card):
            cards_on_board_count = game.round.cards_on_board_count

            # if 1st card played, check for marriage.
            if cards_on_board_count == 1:
                cards_left_in_hand = game.round.seat_infos[card_played_by].hand.cards
                marriage_possible = is_played_card_part_of_marriage(played_card, cards_left_in_hand)

                if not marriage_possible:
                    return None
                else:
                    if played_card.suit == game.round.trump_suit:
                        return MarriagePointsAddedEvent(
                            points=LARGE_MARRIAGE_POINTS,
                            added_to=card_played_by,
                        )
                    elif played_card.suit != game.round.trump_suit and game.round.is_marriage_announced:
                        return MarriagePointsAddedEvent(
                            points=SMALL_MARRIAGE_POINTS,
                            added_to=card_played_by,
                        )

            # if 3rd card played for this trick, then trick is finished
            elif cards_on_board_count == 3:
                cards_on_board = game.round.cards_on_board
                trick_cards = [card for card in cards_on_board.values() if card is not None]
                trick_winning_card = get_trick_winning_card(
                    trick_cards, game.round.required_suit, game.round.trump_suit
                )
                trick_winning_seat = next(seat for seat, card in cards_on_board.items() if card == trick_winning_card)
                return TrickTakenEvent(taken_by=trick_winning_seat, cards=trick_cards)
            return None

        case TrickTakenEvent():
            # if any of seats does not have cards left, then round is finished
            if len(game.active_seats_info.hand.cards) == EMPTY_HAND_SIZE:
                return RoundFinishedEvent(
                    round_number=game.round.round_number,
                    declarer=game.round.highest_bid[0] if game.round.highest_bid else None,
                    given_up=False,
                )
            return None

        case RoundFinishedEvent():
            if any(points <= 0 for points in game.summary.values()):
                return GameEndedEvent(reason=GameEndingReason.FINISHED, seat=None)
            if all(points >= NOT_ALLOWED_TO_BID_THRESHOLD for points in game.summary.values()):
                return GameEndedEvent(reason=GameEndingReason.FINISHED, seat=None)
            if game.round.round_number >= game.game_config.max_rounds:
                return GameEndedEvent(reason=GameEndingReason.FINISHED, seat=None)
            deck = FiveHundredDeck.build()
            return DeckShuffledEvent(deck=deck)

        case _:
            return None
