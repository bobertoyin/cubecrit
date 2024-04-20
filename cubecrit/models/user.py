"""Data models for users."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Connection, text


@dataclass(frozen=True)
class User:
    """A user of the website."""

    wca_id: str
    """The user-facing identifier."""
    joined: datetime
    """The user's join date and time."""
    first_name: str | None
    """User's first name."""
    last_name: str | None
    """User's last name."""
    profile_picture_url: str | None
    """Link to the user's profile picture."""

    @staticmethod
    def get_user(conn: Connection, wca_id: str) -> Optional["User"]:
        """Get a user from the database given a WCA ID.

        Parameters:
            - conn: the database connection
            - wca_id: the user-facing identifier

        Returns a user, or None if the wca_id does not exist.
        """
        with open("cubecrit/sql/get_user.sql") as query:
            result = conn.execute(text(query.read()), {"wca_id": wca_id}).first()
            conn.commit()
            if result is not None:
                return User(**result._asdict())
            return None
