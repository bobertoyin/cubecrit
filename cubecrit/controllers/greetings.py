from flask import Blueprint, render_template

from ..models.greeting import get_greeting
from ..db import db

greetings = Blueprint(
    "greetings", __name__, template_folder="templates", url_prefix="/greetings"
)


@greetings.route("/greet/<string:name>", methods=["GET"])
def greet_user(name: str) -> str:
    with db.connect() as connection:
        return render_template(
            "greeting.html", name=name, greeting=get_greeting(connection)
        )
