from flask import Flask
from sqlalchemy import text

from .db import db

from .controllers.puzzles import puzzles


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(puzzles)

    with db.connect() as connection:
        with app.open_resource("schema.sql") as schema:
            schema_content = str(schema.read(), encoding="utf8")  # type: ignore[call-overload]
            connection.execute(text(schema_content))
            connection.commit()
    return app
