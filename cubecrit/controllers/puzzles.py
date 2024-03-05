from flask import Blueprint, render_template, abort

from ..db import db

from ..models.puzzle import Puzzle

puzzles = Blueprint(
    "puzzles", __name__, template_folder="templates", url_prefix="/puzzles"
)


@puzzles.route("/puzzles/<string:external_id>", methods=["GET"])
def get_puzzle_route(external_id: str) -> str:
    with db.connect() as connection:
        puzzle = Puzzle.get_puzzle(connection, external_id)
        if puzzle is None:
            return abort(404)
        return render_template("puzzles.html", puzzle=puzzle)