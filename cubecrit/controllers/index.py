from flask import Blueprint, render_template

index = Blueprint("index", __name__, template_folder="templates")


@index.route("/")
def get_index_route() -> str:
    return render_template("index.html")
