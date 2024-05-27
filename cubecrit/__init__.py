"""Entry point for the application."""

from flask import Flask
from flask_apscheduler import APScheduler
from sqlalchemy import text

from .controllers.index import index
from .controllers.manufacturers import manufacturers
from .controllers.puzzles import puzzles
from .db import db
from .sync import sync_data, sync_data_with_conn


def create_app() -> Flask:
    """Create the cubecrit flask app.

    Returns the configured flask application object.
    """
    app = Flask(__name__)
    app.register_blueprint(index)
    app.register_blueprint(manufacturers)
    app.register_blueprint(puzzles)

    with db.connect() as connection:
        with app.open_resource("sql/schema.sql") as schema:
            schema_content = str(schema.read(), encoding="utf8")  # type: ignore[call-overload]
            connection.execute(text(schema_content))
            connection.commit()
        sync_data_with_conn(connection)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.add_job(
        "sync_data", sync_data, max_instances=1, trigger="cron", hour="0", minute="0"
    )
    with app.app_context():
        scheduler.start()

    return app
