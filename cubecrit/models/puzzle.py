"""Data models for puzzles."""
from dataclasses import dataclass
from datetime import date
from math import ceil
from typing import Optional

from sqlalchemy import Connection, text

from .manufacturer import Country, Manufacturer

PUZZLES_PER_PAGE = 10


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
    def get_num_pages(
        conn: Connection, q: str | None = None, puzzle_type: str | None = None
    ) -> int:
        """Get the total number of pages of puzzles currently in the database.

        Returns the total number of pages.
        """
        with open("cubecrit/sql/get_num_puzzles.sql") as query:
            result = conn.execute(
                text(query.read()),
                {
                    "puzzle_type": puzzle_type,
                    "q": q,
                },
            )
            conn.commit()
            return ceil(list(result)[0].num_puzzles / PUZZLES_PER_PAGE)

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
                    result.puzzle_type_external_id,
                    result.puzzle_type_display_name,
                )
                country = Country(
                    result.country_external_id, result.country_display_name
                )
                manufacturer = Manufacturer(
                    result.manufacturer_external_id,
                    result.manufacturer_display_name,
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

    @staticmethod
    def get_puzzle_page(
        conn: Connection,
        page_number: int,
        puzzle_type: str | None = None,
        q: str | None = None,
    ) -> list["Puzzle"]:
        """Get a paginated list of puzzles.

        The puzzles are sorted by name in lexicographical order.

        Parameters:
        - conn: the database connection
        - page_number: the page number to retrieve

        Returns a list of puzzles for the page.
        """
        with open("cubecrit/sql/get_puzzle_page.sql") as query:
            result = conn.execute(
                text(query.read()),
                {
                    "puzzles_per_page": PUZZLES_PER_PAGE,
                    "puzzles_offset": (page_number - 1) * PUZZLES_PER_PAGE,
                    "puzzle_type": puzzle_type,
                    "q": q,
                },
            )
            conn.commit()
            puzzle_list = []
            for row in result:
                puzzle_t = PuzzleType(
                    row.puzzle_type_external_id,
                    row.puzzle_type_display_name,
                )
                country = Country(row.country_external_id, row.country_display_name)
                manufacturer = Manufacturer(
                    row.manufacturer_external_id,
                    row.manufacturer_display_name,
                    country,
                )
                puzzle = Puzzle(
                    row.external_id,
                    row.display_name,
                    row.release_date,
                    row.discontinue_date,
                    puzzle_t,
                    manufacturer,
                )
                puzzle_list.append(puzzle)
            return puzzle_list
