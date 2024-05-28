"""Routes for the home page."""
from flask import Blueprint, current_app, render_template

from ..models.puzzle import PuzzleType

index = Blueprint("index", __name__, template_folder="templates")


@index.route("/")
def get_index_route() -> str:
    """Route the user to the home page.

    Returns a rendered HTML template.
    """
    with current_app.config["db"].connect() as connection:
        all_puzzle_types = PuzzleType.get_all_puzzle_types(connection)
        return render_template("index.html", all_puzzle_types=all_puzzle_types)
