"""Routes for puzzle-related pages."""
from flask import Blueprint, abort, render_template

from ..db import db
from ..models.puzzle import Puzzle

puzzles = Blueprint(
    "puzzles", __name__, template_folder="templates", url_prefix="/puzzles"
)


@puzzles.route("/<string:external_id>", methods=["GET"])
def get_puzzle_route(external_id: str) -> str:
    """Get a single puzzle.

    Parameters:
    - external_id: The external ID of the puzzle.

    Raises:
    - a 404 error if there is no puzzle found

    Returns an HTML page.
    """
    with db.connect() as connection:
        puzzle = Puzzle.get_puzzle(connection, external_id)
        if puzzle is None:
            raise abort(404)
        return render_template("puzzle.html", puzzle=puzzle)
