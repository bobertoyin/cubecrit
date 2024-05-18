from flask import Blueprint, abort, render_template, request

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
            raise abort(404)
        return render_template("puzzle.html", puzzle=puzzle)


@puzzles.route("/", methods=["GET"])
def get_puzzle_page_route() -> str:
    page = validate_page_number(request.args.get("page"))
    with db.connect() as connection:
        num_pages = Puzzle.get_num_pages(connection)
        if page > num_pages or page < 1:
            raise abort(404)
        puzzle_page = Puzzle.get_puzzle_page(connection, page)
        return render_template(
            "puzzles.html", puzzle_page=puzzle_page, page=page, num_pages=num_pages
        )


def validate_page_number(page_number: str | None) -> int:
    if page_number is None:
        return 1
    try:
        check_num = int(page_number)
        return check_num
    except ValueError:
        return 1
