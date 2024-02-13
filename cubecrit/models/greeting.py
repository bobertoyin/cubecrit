from dataclasses import dataclass

from sqlalchemy import Connection, text


@dataclass(frozen=True)
class Greeting:
    greeting: str


def get_greeting(conn: Connection) -> Greeting | None:
    result = conn.execute(
        text("SELECT greeting FROM greetings ORDER BY random()")
    ).first()
    conn.commit()
    if result is not None:
        return Greeting(**result._asdict())
    return result
