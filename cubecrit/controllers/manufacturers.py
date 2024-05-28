"""Routes for manufacturer-related pages."""
from flask import Blueprint, abort, current_app, render_template

from ..models.manufacturer import Manufacturer

manufacturers = Blueprint(
    "manufacturers", __name__, template_folder="templates", url_prefix="/manufacturers"
)


@manufacturers.route("/<string:external_id>", methods=["GET"])
def get_manufacturer_route(external_id: str) -> str:
    """Get a single manufacturer.

    Parameters:
    - external_id: The external ID of the manufacturer.

    Raises:
    - a 404 error if there is no manufacturer found

    Returns an HTML page.
    """
    with current_app.config["db"].connect() as connection:
        manufacturer = Manufacturer.get_manufacturer(connection, external_id)
        if manufacturer is None:
            raise abort(404)
        return render_template("manufacturer.html", manufacturer=manufacturer)
