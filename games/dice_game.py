# games/dice_game.py

class DiceGame:
    """
    Simple craps-like dice game:
    - Turn 1: 2,3,12 lose | 7,11 win | otherwise set 'point' and continue
    - Turn 2+: 7 lose | point wins | otherwise keep rolling
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.turn = 1
        self.point = None
        self.finished = False
        self.last_roll = None
        self.result = ""

    def apply_roll(self, roll: int) -> str:
        """Apply a validated roll (2-12) and return a result message."""
        if self.finished:
            return "Game is finished. Start a new game to play again."

        self.last_roll = roll

        # Turn 1 rules
        if self.turn == 1:
            if roll in (2, 3, 12):
                self.finished = True
                self.result = f"Turn {self.turn}: Rolled {roll}. You LOSE."
                return self.result

            if roll in (7, 11):
                self.finished = True
                self.result = f"Turn {self.turn}: Rolled {roll}. You WIN!"
                return self.result

            # Otherwise set point and move to next turn
            self.point = roll
            self.turn += 1
            self.result = f"Turn 1: Rolled {roll}. Point is set to {self.point}. Continue..."
            return self.result

        # Turn 2+ rules
        if roll == 7:
            self.finished = True
            self.result = f"Turn {self.turn}: Rolled 7. You LOSE."
            return self.result

        if roll == self.point:
            self.finished = True
            self.result = f"Turn {self.turn}: Rolled {roll} (your point). You WIN!"
            return self.result

        # No decision; go to next turn
        self.turn += 1
        self.result = f"Turn {self.turn - 1}: Rolled {roll}. No win/lose. Roll again..."
        return self.result


def parse_roll(text: str):
    """
    Returns (roll_int, error_message)
    roll_int is None if invalid.
    Accepts 'q' or 'quit' as quit commands.
    """
    text = text.strip().lower()

    if text in ("q", "quit"):
        return None, "QUIT"

    if not text.isdigit():
        return None, "Error: Please enter a number between 2 and 12 (or 'q' to quit)."

    roll = int(text)
    if roll < 2 or roll > 12:
        return None, "Error: Dice roll must be between 2 and 12."

    return roll, None


def play_cli():
    """Command-line version for controlled test data."""
    game = DiceGame()

    print("\nDice Game (CLI)")
    print("Enter a roll (2-12). Type 'q' to quit.\n")

    while True:
        if game.finished:
            print("\nGame over.")
            again = input("Type 'new' to start a new game, or 'q' to quit: ").strip().lower()
            if again in ("q", "quit"):
                print("Goodbye!")
                break
            if again == "new":
                game.reset()
                print("\n--- New Game ---\n")
            else:
                print("Please type 'new' or 'q'.")
            continue

        user_in = input(f"Turn {game.turn} - Enter roll (2-12): ")
        roll, err = parse_roll(user_in)

        if err == "QUIT":
            print("Goodbye!")
            break

        if err:
            print(err)
            print()
            continue

        message = game.apply_roll(roll)
        print(message)
        print()  # blank line for readability
