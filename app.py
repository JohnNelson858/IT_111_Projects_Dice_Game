# app.py
"""
John Nelson - IT 111 - Introduction to Python Programming
Assignment 3: Dice Game in Python
"""

"""
This app.py is turning this dice game logic into a web app by:

1) showing a page (GET)

2) receiving form input (POST)

3) validating the input

4) updating the DiceGame object

5) saving the game state in session so it persists across clicks

6) rendering the updated page again
"""

from flask import Flask, render_template, request, session    # Flask creates the app
                                                              # render_template loads templates/dice.html and fills in variables
                                                              # request gives access to form data from the browser
                                                              # session is a per-user storage space (cookie-based) that lets the game “remember” state between requests
from games.dice_game import DiceGame, parse_roll              # DiceGame and parse_roll are logic from games/dice_game.py

app = Flask(__name__)                                         # Creates the app object
app.secret_key = "random-secret-key"                          # Flask signs session data so users can’t easily tamper with it


def load_game() -> DiceGame:
    """Load game from session or create a new one."""
    data = session.get("game")                                # Looks inside the session for a key named "game". If it’s not there yet (first visit), data is None
    game = DiceGame()                                         # Creates a fresh new game object

    if data:                                                  # If session has saved game info, copy those values into the new game object
        game.turn = data.get("turn", 1)
        game.point = data.get("point", None)
        game.finished = data.get("finished", False)
        game.last_roll = data.get("last_roll", None)
        game.result = data.get("result", "")

    return game


def save_game(game: DiceGame) -> None:
    """Converts DiceGame object into a plain dictionary and saves it to session["game"]"""
    session["game"] = {
        "turn": game.turn,
        "point": game.point,
        "finished": game.finished,
        "last_roll": game.last_roll,
        "result": game.result,
    }


""" Routes: / and /dice both go to the same function
    http://127.0.0.1:5000/ or http://127.0.0.1:5000/dice
"""
@app.route("/", methods=["GET", "POST"])
@app.route("/dice", methods=["GET", "POST"])
def dice():
    game = load_game()                                                # Load the saved game (or start new)
    error = ""                                                        # error holds any validation message to show the user in the HTML

    if request.method == "POST":                                      # Tells whether this is a normal page load (GET) or a form submission (POST)
        action = request.form.get("action", "roll")                   # Contains data from HTML form inputs

        """ action will be "roll" or "new" based on which button they clicked """
        if action == "new":
            game.reset()                                              # Reset the game state
            save_game(game)                                           # Save it
            return render_template("dice.html", game=game, error="")  # Immediately render the page again with the reset state

        """ If they clicked Submit Roll: read and validate the roll """
        roll_text = request.form.get("roll", "")                      # Gets the text typed in the input box named "roll"
        roll, err = parse_roll(roll_text)                             # Returns roll (int) and err=None if good; or roll=None and an error message or roll=None and "QUIT"

        if err == "QUIT":
            game.reset()                                              # Resets the game
            game.result = "Game ended. Start a new game."             # Set a message
            save_game(game)                                           # Saves and re-renders
            return render_template("dice.html", game=game, error="")

        if err:
            error = err                                               # If err is a normal string error message, store it in error
        else:
            game.apply_roll(roll)                                     # Apply the roll to the game rules

        save_game(game)                                               # Makes the game continue across multiple POSTs


    return render_template("dice.html", game=game, error=error)       # Loads templates/dice.html and gives it game and error

if __name__ == "__main__":
    app.run(debug=True)
