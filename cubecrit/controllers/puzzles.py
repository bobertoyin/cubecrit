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
            return abort(404)
        return render_template("puzzle.html", puzzle=puzzle)


@puzzles.route("/", methods=["GET"])
def get_puzzle_page_route() -> str:
    page = request.args.get("page")
    with db.connect() as connection:
        puzzle_page = Puzzle.get_puzzle_page(connection, validate_page_number(page))
        return render_template("puzzles.html", puzzle_page=puzzle_page)


def validate_page_number(page_number: str | None) -> int:
    if page_number is None:
        return 1
    try:
        check_num = int(page_number)
        if check_num <= 0:
            check_num = 1
        return check_num
    except ValueError:
        return 1
