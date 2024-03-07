from dataclasses import dataclass
from datetime import date
from sqlalchemy import Connection, text
from typing import Optional

from .manufacturer import Manufacturer, Country


@dataclass(frozen=True)
class PuzzleType:
    external_id: str
    display_name: str

    @staticmethod
    def get_puzzle_type(conn: Connection, external_id: str) -> Optional["PuzzleType"]:
        with open("cubecrit/sql/get_puzzle_type.sql") as query:
            result = conn.execute(
                text(query.read()), {"external_id": external_id}
            ).first()
            conn.commit()
            if result is not None:
                return PuzzleType(**result._asdict())
            return None


@dataclass(frozen=True)
class Puzzle:
    external_id: str
    display_name: str
    release_date: date | None
    discontinue_date: date | None
    puzzle_type: PuzzleType
    manufacturer: Manufacturer

    @staticmethod
    def get_puzzle(conn: Connection, external_id: str) -> Optional["Puzzle"]:
        """Get a puzzle from the database given an external ID.

        Parameters:
            -conn: the database connection
            -external_id: the user-facing identifier

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


# MAKE USERS CLASS AND METHOD
# MAKE REVIEWS CLASS AND METHOD
