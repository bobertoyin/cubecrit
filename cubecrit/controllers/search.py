from flask import Blueprint, render_template, request

from ..db import db
from ..models.puzzle import Puzzle

search = Blueprint(
    "search", __name__, template_folder="templates", url_prefix="/search"
)


@search.route("/", methods=["GET"])
def get_search_route() -> str:
    puzzle_type = request.args.get("puzzle_type")
    if puzzle_type and puzzle_type.strip() == "":
        puzzle_type = None
    query = request.args.get("query")
    if query and query.strip() == "":
        query = None
    with db.connect() as connection:
        puzzles = Puzzle.get_puzzle_page(connection, 1, puzzle_type, query)
        return render_template("search.html", puzzles=puzzles)
