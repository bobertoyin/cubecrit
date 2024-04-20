"""Data models for puzzles."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

from sqlalchemy import Connection, text

from .manufacturer import Country, Manufacturer


@dataclass(frozen=True)
class PuzzleType:
    """A type of puzzle."""

    external_id: str
    """The user-facing identifier."""
    display_name: str
    """The formatted display name."""

    @staticmethod
    def get_puzzle_type(conn: Connection, external_id: str) -> Optional["PuzzleType"]:
        """Get a type of puzzle from the database given an external ID.

        Parameters:
        - conn: the database connection
        - external_id: the user-facing identifier

        Returns a puzzle type, or None if the external ID does not exist.
        """
        with open("cubecrit/sql/get_puzzle_type.sql") as query:
            result = conn.execute(
                text(query.read()), {"external_id": external_id}
            ).first()
            conn.commit()
            if result is not None:
                return PuzzleType(**result._asdict())
            return None

    @staticmethod
    def get_all_puzzle_types(conn: Connection) -> list["PuzzleType"]:
        """Get all puzzle types from the database.

        Parameters:
        - conn: the database connection

        Returns a list of puzzle types.
        """
        with open("cubecrit/sql/get_all_puzzle_types.sql") as query:
            result = conn.execute(text(query.read()))
            conn.commit()
            puzzle_type_list = []
            for row in result:
                puzzle_type_list.append(PuzzleType(**row._asdict()))
            return puzzle_type_list


@dataclass(frozen=True)
class Puzzle:
    """A puzzle."""

    external_id: str
    """User-facing identifier for the puzzle."""
    display_name: str
    """The formatted display name."""
    release_date: date | None
    """The date when the puzzle was released."""
    discontinue_date: date | None
    """The date when the puzzle was discontinued."""
    puzzle_type: PuzzleType
    """The type of puzzle."""
    manufacturer: Manufacturer
    """The manufacturer of the puzzle."""

    @staticmethod
    def get_puzzle(conn: Connection, external_id: str) -> Optional["Puzzle"]:
        """Get a puzzle from the database given an external ID.

        Parameters:
            - conn: the database connection
            - external_id: the user-facing identifier

        Returns a puzzle, or None if the external ID does not exist.
        """
        with open("cubecrit/sql/get_puzzle.sql") as query:
            result = conn.execute(
                text(query.read()), {"external_id": external_id}
            ).first()
            conn.commit()
            if result is not None:
                puzzle_type = PuzzleType(
                    result.puzzle_types_external_id,
                    result.puzzle_types_display_name,
                )
                country = Country(
                    result.countries_external_id, result.countries_display_name
                )
                manufacturer = Manufacturer(
                    result.manufacturers_external_id,
                    result.manufacturers_display_name,
                    country,
                )
                return Puzzle(
                    result.external_id,
                    result.display_name,
                    result.release_date,
                    result.discontinue_date,
                    puzzle_type,
                    manufacturer,
                )
            return None
