from backend.games.five_hundred.domain.five_hundred_card import FiveHundredCard
from backend.games.five_hundred.domain.five_hundred_deck import FiveHundredDeck
from backend.games.five_hundred.domain.five_hundred_command import (
    MakeBidCommand,
    PassCardsCommand,
    PlayCardCommand,
)
from backend.games.five_hundred.domain.five_hundred_game import FiveHundredGame
from backend.games.five_hundred.domain.five_hundred_phase import FiveHundredPhase
from backend.games.five_hundred.domain.five_hundred_round import FiveHundredRound
from backend.games.five_hundred.domain.five_hundred_seat import FiveHundredSeat
from backend.games.five_hundred.process_command import process_command


def main() -> None:

    def repl():

        deck = FiveHundredDeck.build()

        game = FiveHundredGame.create(FiveHundredRound.create(deck, 1, FiveHundredSeat.ONE))
        print("\nWelcome to Five Hundred!")

        while True:
            print(f"\n{game}")

            match game.round.phase:
                case FiveHundredPhase.BIDDING:
                    print("\nEnter bid amount (60 -> 200) or negative number to pass:")
                    try:
                        bid = int(input("> "))
                        cmd = MakeBidCommand(type="MAKE_BID", bid=bid)
                        game = process_command(game, cmd)[0]
                    except ValueError:
                        print("Invalid input! Please enter a number.")
                        continue

                case FiveHundredPhase.FORMING_HANDS:
                    print("\nEnter two cards to pass (e.g. 'Ah Kd'):")
                    try:
                        card1_str, card2_str = input("> ").split()
                        cards = list(game.round.active_seats_info.hand.cards)

                        # Find the matching cards in hand
                        card1 = next(
                            (c for c in cards if c == FiveHundredCard.from_string(card1_str)),
                            None,
                        )
                        card2 = next(
                            (c for c in cards if c == FiveHundredCard.from_string(card2_str)),
                            None,
                        )

                        if card1 is None or card2 is None:
                            raise ValueError("Card not found in hand")

                        cmd = PassCardsCommand(
                            type="PASS_CARDS",
                            card_to_next_seat=card1,
                            card_to_prev_seat=card2,
                        )
                        game = process_command(game, cmd)[0]
                    except (ValueError, IndexError):
                        print("Invalid input! Please enter two valid cards (e.g. 'Ah Kd')")
                        continue

                case FiveHundredPhase.PLAYING_CARDS:
                    allowed_cards = game.round.active_seats_info.cards_allowed_to_play(
                        game.round.required_suit, game.round.trump_suit
                    )
                    print(
                        "\nYour allowed cards:",
                        " ".join(str(card) for card in allowed_cards),
                    )
                    print("\nEnter card to play (e.g. 'Ah'):")
                    try:
                        card_str = input("> ")
                        card = next(
                            (c for c in allowed_cards if c == FiveHundredCard.from_string(card_str)),
                            None,
                        )
                        if card is None:
                            raise ValueError("Card not found or not allowed")
                        cmd = PlayCardCommand(type="PLAY_CARD", card=card)
                        game = process_command(game, cmd)[0]
                    except (ValueError, IndexError):
                        print("Invalid input! Please enter a valid card (e.g. 'Ah')")
                        continue

                case FiveHundredPhase.FINISHING_ROUND | FiveHundredPhase.GAME_FINISHED:
                    print("\nGame over! Final scores:")
                    for seat, points in game.summary.items():
                        print(f"Seat {seat}: {points}")
                    return

    repl()


if __name__ == "__main__":
    main()
