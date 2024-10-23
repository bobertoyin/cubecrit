"""Functions for synchronizing database data."""
from csv import DictReader
from typing import Any, TypeAlias

from flask_apscheduler import APScheduler
from sqlalchemy import Connection, text

CSVRow: TypeAlias = dict[str | Any, str | Any | None]

scheduler = APScheduler()


@scheduler.task("cron", max_instances=1, hour="0", minute="0")
def sync_data() -> None:
    """Synchronize the database with data from `cubecrit-data`."""
    with scheduler.app.config["db"].connect() as conn:
        sync_data_with_conn(conn)


def sync_data_with_conn(conn: Connection) -> None:
    """Synchronize the database with data from `cubecrit-data` and a database connection.

    Parameters:
        - conn: the database connection
    """
    _sync_data_delegate(conn, "puzzle_types")
    _sync_data_delegate(conn, "countries")
    _sync_data_delegate(conn, "manufacturers")
    _sync_data_delegate(conn, "puzzles")
    conn.commit()


def _sync_data_delegate(conn: Connection, name: str) -> None:
    """Delegate synchronizing database data from `cubecrit-data`.

    Parameters:
        - conn: the database connection
        - name: the name of the CSV file for downloading and the name of the query for updating
                CSV file will be under `<name>.csv` in `cubecrit-data` and SQL will be under `sql/sync/<name>.sql`
    """
    data = _extract_data(name)

    with open(f"cubecrit/sql/sync/{name}.sql") as query:
        conn.execute(text(query.read()), data)


def _extract_data(name: str) -> list[CSVRow]:
    """Extract data from `cubecrit-data`.

    Parameters:
        - name: the name of the CSV file to pull from

    Returns a list of rows from the CSV file.
    """
    # open file from url -> buffer the text stream -> read CSV into list of dictionaries -> handle empty string values
    with open(f"cubecrit/data/{name}.csv") as file:
        return [
            _replace_empty_string(row)
            # suppressing lint because we're going to move away from remote CSV soon
            for row in DictReader(file)
        ]


def _replace_empty_string(
    row: CSVRow,
) -> CSVRow:
    """Replace empty string values in a CSV row with None.

    Necessary to properly handle empty cells that are read from CSV files.

    Does not modify the keys.

    Parameters:
        - row: The row to process.

    Returns a processed row with empty string values replaced with None.
    """
    return {k: v if v != "" else None for k, v in row.items()}
