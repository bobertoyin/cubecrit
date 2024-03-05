from typing import Any, Generator

from pytest import fixture
from sqlalchemy import Connection, create_engine, text

engine = create_engine("postgresql://test:password@localhost:5433/test")


@fixture
def db_connection() -> Generator[Connection, Any, Any]:
    connection = engine.connect()
    reset_query = text(
        """
        SELECT 'DROP TABLE IF EXISTS "' || tablename || '" CASCADE;' FROM
        pg_tables WHERE schemaname = 'public';
        """
    )
    connection.execute(reset_query)
    with open("cubecrit/schema.sql") as schema:
        connection.execute(text(schema.read()))
    with open("cubecrit/seed.sql") as seed:
        connection.execute(text(seed.read()))
    connection.commit()
    yield connection
    connection.execute(reset_query)
    connection.commit()
    connection.close()
