from flask import Blueprint, render_template

from ..db import db
from ..models.puzzle import PuzzleType

index = Blueprint("index", __name__, template_folder="templates")


@index.route("/")
def get_index_route() -> str:
    with db.connect() as connection:
        all_puzzle_types = PuzzleType.get_all_puzzle_types(connection)
    return render_template("index.html", all_puzzle_types=all_puzzle_types)
