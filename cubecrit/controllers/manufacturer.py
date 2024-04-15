from flask import Blueprint, abort, render_template

from ..db import db
from ..models.manufacturer import Manufacturer

manufacturer = Blueprint(
    "manufacturer", __name__, template_folder="templates", url_prefix="/manufacturers"
)


@manufacturer.route("/<string:external_id>", methods=["GET"])
def get_manufacturer_route(external_id: str) -> str:
    with db.connect() as connection:
        manufacturer = Manufacturer.get_manufacturer(connection, external_id)
        if manufacturer is None:
            return abort(404)
        return render_template("manufacturer.html", manufacturer=manufacturer)
