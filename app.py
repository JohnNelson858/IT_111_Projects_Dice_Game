# app.py

from flask import Flask, render_template, request, session
from games.dice_game import DiceGame, parse_roll

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key"


def load_game() -> DiceGame:
    """Load game from session or create a new one."""
    data = session.get("game")
    game = DiceGame()

    if data:
        game.turn = data.get("turn", 1)
        game.point = data.get("point", None)
        game.finished = data.get("finished", False)
        game.last_roll = data.get("last_roll", None)
        game.result = data.get("result", "")

    return game


def save_game(game: DiceGame) -> None:
    """Save game to session."""
    session["game"] = {
        "turn": game.turn,
        "point": game.point,
        "finished": game.finished,
        "last_roll": game.last_roll,
        "result": game.result,
    }


@app.route("/", methods=["GET", "POST"])
@app.route("/dice", methods=["GET", "POST"])
def dice():
    game = load_game()
    error = ""

    if request.method == "POST":
        action = request.form.get("action", "roll")

        if action == "new":
            game.reset()
            save_game(game)
            return render_template("dice.html", game=game, error="")

        roll_text = request.form.get("roll", "")
        roll, err = parse_roll(roll_text)

        if err == "QUIT":
            game.reset()
            game.result = "Game ended. Start a new game."
            save_game(game)
            return render_template("dice.html", game=game, error="")

        if err:
            error = err
        else:
            game.apply_roll(roll)

        save_game(game)

    return render_template("dice.html", game=game, error=error)


if __name__ == "__main__":
    app.run(debug=True)
