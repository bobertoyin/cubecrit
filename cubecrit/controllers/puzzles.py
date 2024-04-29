from flask import Blueprint, abort, render_template

from ..db import db
from ..models.puzzle import Puzzle

puzzles = Blueprint(
    "puzzles", __name__, template_folder="templates", url_prefix="/puzzles"
)


@puzzles.route("/<string:external_id>", methods=["GET"])
def get_puzzle_route(external_id: str) -> str:
    with db.connect() as connection:
        puzzle = Puzzle.get_puzzle(connection, external_id)
        if puzzle is None:
            return abort(404)
        return render_template("puzzle.html", puzzle=puzzle)


@puzzles.route("/", methods=["GET"])
def get_all_puzzles_route() -> str:
    with db.connect() as connection:
        all_puzzles = Puzzle.get_all_puzzles(connection)
        return render_template("all_puzzles.html", all_puzzles=all_puzzles)
