from flask import Blueprint, render_template

from ..db import db

greetings = Blueprint(
    "greetings", __name__, template_folder="templates", url_prefix="/greetings"
)


@greetings.route("/greet/<string:name>", methods=["GET"])
def greet_user(name: str) -> str:
    with db.connect() as _connection:
        return render_template("greeting.html", name=name, greeting="HI")
