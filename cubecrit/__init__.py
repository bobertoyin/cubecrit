"""Entry point for the application."""
from os import environ

from flask import Flask
from sqlalchemy import text

from .controllers.index import index
from .controllers.manufacturers import manufacturers
from .controllers.puzzles import puzzles
from .controllers.search import search
from .db import db


def create_app() -> Flask:
    """Create the cubecrit flask app.

    Returns the configured flask application object.
    """
    app = Flask(__name__)
    app.register_blueprint(index)
    app.register_blueprint(manufacturers)
    app.register_blueprint(puzzles)
    app.register_blueprint(search)

    with db.connect() as connection:
        sql_files = ["schema.sql"]
        if environ.get("DB_SEED") == "1":
            sql_files.append("seed.sql")
        for sql_file in sql_files:
            with app.open_resource(f"sql/{sql_file}") as schema:
                schema_content = str(schema.read(), encoding="utf8")  # type: ignore[call-overload]
                connection.execute(text(schema_content))
        connection.commit()

    return app
