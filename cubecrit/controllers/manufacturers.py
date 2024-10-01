"""Routes for manufacturer-related pages."""
from flask import Blueprint, abort, current_app, render_template, request

from ..models.manufacturer import Manufacturer
from ..models.puzzle import Puzzle
from ..validate import validate_page_number

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
        num_pages = Puzzle.get_num_pages(connection)
        manufacturer = Manufacturer.get_manufacturer(connection, external_id)
        if manufacturer is None:
            raise abort(404)
        try:
            page = validate_page_number(request.args.get("page"), num_pages)
        except ValueError:
            raise abort(404)
        puzzle_page = Puzzle.get_puzzle_page(
            connection, page, manufacturer=manufacturer
        )
        return render_template(
            "manufacturer.html",
            manufacturer=manufacturer,
            puzzle_page=puzzle_page,
            num_pages=num_pages,
            page=page,
        )
