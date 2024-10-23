"""Entry point for the application."""
from os import environ

from flask import Flask
from sqlalchemy import create_engine, text

from .controllers.index import index
from .controllers.manufacturers import manufacturers
from .controllers.puzzles import puzzles
from .controllers.search import search
from .sync import scheduler, sync_data_with_conn


def create_app() -> Flask:
    """Create the cubecrit flask app.

    Returns the configured flask application object.
    """
    db_addr = environ["DB_ADDRESS"]

    app = Flask(__name__)
    app.config["db"] = create_engine(db_addr)
    app.register_blueprint(index)
    app.register_blueprint(manufacturers)
    app.register_blueprint(puzzles)
    app.register_blueprint(search)

    with app.config["db"].connect() as connection:
        with app.open_resource("sql/schema.sql") as schema:
            schema_content = str(schema.read(), encoding="utf8")  # type: ignore[call-overload]
            connection.execute(text(schema_content))
            connection.commit()
        sync_data_with_conn(connection)

    scheduler.init_app(app)
    with app.app_context():
        scheduler.start()

    return app
