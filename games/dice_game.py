"""
John Nelson - IT 111 - Introduction to Python Programming
Assignment 3: Dice Game in Python
"""
# games/dice_game.py

class DiceGame:                       # The container that holds all of that state and the methods that update it
    """
    Simple craps-like dice game:
    - Turn 1: 2,3,12 lose | 7,11 win | otherwise set 'point' and continue
    - Turn 2+: 7 lose | point wins | otherwise keep rolling
    """

    def __init__(self):               # Lets you read/write variables that belong to that object
        self.reset()

    def reset(self):                  # Start a brand-new game function
        self.turn = 1                 # First roll of a new game
        self.point = None             # No point has been set yet
        self.finished = False         # The game is not over yet
        self.last_roll = None         # No roll has happened yet in the new game
        self.result = ""              # Clears the message shown to the player

    """ apply_roll() is called every time the user submits a roll """
    def apply_roll(self, roll: int) -> str:  # Method is apply_roll - takes one input self:roll which should be an integer and returns a string
        """Apply a validated roll (2-12) and return a result message."""
        if self.finished:             # If the game is already over refuse to process another roll
            return "Game is finished. Start a new game to play again."

        self.last_roll = roll         # Stores the current roll inside the object so it can be displayed later

        # Turn 1 rules
        if self.turn == 1:            # Skip entire block if not turn 1
            if roll in (2, 3, 12):    # If one of these values then player craps out
                self.finished = True  # End the game
                self.result = f"Turn {self.turn}: Rolled {roll}. You LOSE."                     # Store a message
                return self.result    # Exits the function immediately

            if roll in (7, 11):       # Rolling 7 or 11 on the first turn ends the game with a win.
                self.finished = True  # End the game
                self.result = f"Turn {self.turn}: Rolled {roll}. You WIN!"                      # Store a message
                return self.result    # Exits the function immediately

            # Otherwise set point and move to next turn - must be one of: 4, 5, 6, 8, 9, 10
            self.point = roll         # Target number to hit
            self.turn += 1            # Increases turn number
            self.result = f"Turn 1: Rolled {roll}. Point is set to {self.point}. Continue..."   # Stores a message
            return self.result        # Ends the function after setting up the next phase of the game
            """ once you know the outcome for turn 1, you don’t want the function to keep running """

        """ This block runs only after Turn 1 didn’t end the game """
        # Turn 2+ rules
        if roll == 7:                 # Checks if the current roll equals 7
            self.finished = True      # Ends the game
            self.result = f"Turn {self.turn}: Rolled 7. You LOSE."                              # Stores a message
            return self.result        # Ends the function        

        if roll == self.point:        # Checks whether the roll equals the saved point number
            self.finished = True      # Ends the game
            self.result = f"Turn {self.turn}: Rolled {roll} (your point). You WIN!"             # Stores a message
            return self.result        # Ends the function

        # No decision; go to next turn
        self.turn += 1                # Increases turn number
        self.result = f"Turn {self.turn - 1}: Rolled {roll}. No win/lose. Roll again..."        # Stores a message that refers to the turn that just happened
        return self.result            # Ends the function


""" input-validation helper - function that takes text -  type hint (helpful for reading; not enforced automatically) """
def parse_roll(text: str):
    """
    Returns (roll_int, error_message)
    roll_int is None if invalid.
    Accepts 'q' or 'quit' as quit commands.
    """
    text = text.strip().lower()       # Removes leading/trailing spaces and converts to lowercase

    if text in ("q", "quit"):
        return None, "QUIT"           # Function returns None with a message

    if not text.isdigit():
        return None, "Error: Please enter a number between 2 and 12 (or 'q' to quit)."          # If not digits then return None and a message

    roll = int(text)                  # Convert to integer
    if roll < 2 or roll > 12:         # Check range and reject anythibg outside
        return None, "Error: Dice roll must be between 2 and 12."                               # Return None and a message

    return roll, None                 # If everything is good, return the ingeter roll and None for error


"""
Command-line driver for game - main loop

1) shows prompts

2) reads user input

3) validates it (parse_roll)

4) applies rules (apply_roll)

5) prints results

6) repeats until user quits
"""
def play_cli():
    
    game = DiceGame()                   # creates a new game object and (because of __init__) automatically calls reset()

    print("\nDice Game (CLI)")          # Show title and instructions
    print("Enter a roll (2-12). Type 'q' to quit.\n")

    while True:                         # Infinite loop: keep the game running
        """ If the game already ended: ask “new” or “quit” """
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
            continue                    # Bad input path - jumps back to the top of the while True loop so it doesn’t run the “enter roll” logic.

        """ Normal play: ask for a roll and validate it """
        user_in = input(f"Turn {game.turn} - Enter roll (2-12): ")
        roll, err = parse_roll(user_in) # Returns two values: roll (an int if valid, or None) | err (either "QUIT", an error message, or None)

        if err == "QUIT":
            print("Goodbye!")
            break                       # Leave the loop and exit the game

        if err:                         # Handle input errors (not a number, out of range)
            print(err)
            print()
            continue                    # Go back to the top of the loop to ask again (without applying a roll)

        """ Apply the roll to the game rules + print result """
        message = game.apply_roll(roll)
        print(message)
        print()  # blank line for readability
