"""Routes for search pages."""
from flask import Blueprint, abort, current_app, render_template, request

from ..models.puzzle import Puzzle, PuzzleType
from ..validate import validate_page_number, validate_query

search = Blueprint(
    "search", __name__, template_folder="templates", url_prefix="/search"
)


@search.route("/", methods=["GET"])
def get_search_route() -> str:
    """Get a search for puzzles.

    Raises:
    - a 404 error if the page number is invalid.

    Returns an HTML page.
    """
    puzzle_type = request.args.get("puzzle_type")
    if puzzle_type is not None and puzzle_type.strip() == "":
        puzzle_type = None
    query = validate_query(request.args.get("query"))
    with current_app.config["db"].connect() as connection:
        all_puzzle_types = PuzzleType.get_all_puzzle_types(connection)
        num_pages = Puzzle.get_num_pages(connection, query, puzzle_type)
        try:
            page = validate_page_number(request.args.get("page"), num_pages)
        except ValueError:
            raise abort(404)
        puzzles = Puzzle.get_puzzle_page(connection, page, puzzle_type, query)
        return render_template(
            "search.html",
            puzzles=puzzles,
            query=query,
            num_pages=num_pages,
            all_puzzle_types=all_puzzle_types,
            page=page,
            puzzle_type=puzzle_type,
        )
