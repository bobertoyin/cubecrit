"""Routes for puzzle-related pages."""
from flask import Blueprint, abort, current_app, render_template, request

from ..models.puzzle import Puzzle
from ..validate import validate_page_number

puzzles = Blueprint(
    "puzzles", __name__, template_folder="templates", url_prefix="/puzzles"
)


@puzzles.route("/<string:external_id>", methods=["GET"])
def get_puzzle_route(external_id: str) -> str:
    """Get a single puzzle.

    Parameters:
    - external_id: the external ID of the puzzle

    Raises:
    - a 404 error if there is no puzzle found

    Returns an HTML page.
    """
    with current_app.config["db"].connect() as connection:
        puzzle = Puzzle.get_puzzle(connection, external_id)
        if puzzle is None:
            raise abort(404)
        return render_template("puzzle.html", puzzle=puzzle)


@puzzles.route("/", methods=["GET"])
def get_puzzle_page_route() -> str:
    """Get a paginated response of all puzzles.

    Query parameters:
    - page: the page number to retrieve
            if it's not a valid number or not provided, then we default to the first page

    Raises:
    - a 404 error if the page number is too large or too small

    Returns an HTML page.
    """
    with current_app.config["db"].connect() as connection:
        num_pages = Puzzle.get_num_pages(connection)
        try:
            page = validate_page_number(request.args.get("page"), num_pages)
        except ValueError:
            raise abort(404)
        puzzle_page = Puzzle.get_puzzle_page(connection, page)
        return render_template(
            "puzzles.html", puzzle_page=puzzle_page, page=page, num_pages=num_pages
        )
