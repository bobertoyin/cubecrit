from dataclasses import dataclass
from datetime import date
from sqlalchemy import Connection, text
from typing import Optional


@dataclass(frozen=True)
class PuzzleType:
    external_id: str
    display_name: str

    @staticmethod
    def get_puzzle_type(conn: Connection, external_id: str) -> Optional["PuzzleType"]:
        result = conn.execute(
            text(
                "SELECT external_id, display_name FROM puzzle_types WHERE external_id = :external_id"
            ),
            {"external_id": external_id},
        ).first()
        conn.commit()
        if result is not None:
            return PuzzleType(**result._asdict())
        return None


@dataclass(frozen=True)
class Country:
    external_id: str
    display_name: str

    @staticmethod
    def get_country(conn: Connection, external_id: str) -> Optional["Country"]:
        result = conn.execute(
            text(
                "SELECT external_id, display_name FROM countries WHERE external_id = :external_id"
            ),
            {"external_id": external_id},
        ).first()
        conn.commit()
        if result is not None:
            return Country(**result._asdict())
        return None


@dataclass(frozen=True)
class Manufacturer:
    external_id: str
    display_name: str
    country: Country

    @staticmethod
    def get_manufacturer(
        conn: Connection, external_id: str
    ) -> Optional["Manufacturer"]:
        result = conn.execute(
            text(
                """SELECT manufacturers.external_id, countries.external_id as countries_external_id,
                    manufacturers.display_name, countries.display_name as countries_display_name
                    FROM manufacturers
                    JOIN countries ON manufacturers.country_id = countries.id
                    WHERE manufacturers.external_id = :external_id
                    """
            ),
            {"external_id": external_id},
        ).first()
        conn.commit()
        if result is not None:
            country = Country(
                external_id=result.countries_external_id,
                display_name=result.countries_display_name,
            )
            return Manufacturer(
                country=country,
                external_id=result.external_id,
                display_name=result.display_name,
            )
        return None


@dataclass(frozen=True)
class Puzzle:
    external_id: str
    display_name: str
    release_date: date | None
    discontinue_date: date | None
    puzzle_type: PuzzleType

    @staticmethod
    def get_puzzle(conn: Connection, external_id: str) -> Optional["Puzzle"]:
        result = conn.execute(
            text(
                """SELECT puzzles.external_id, puzzle_types.external_id as puzzle_types_external_id, 
                        puzzles.display_name, puzzle_types.display_name as puzzle_types_display_name, 
                        release_date, discontinue_date FROM puzzles 
                JOIN puzzle_types 
                ON puzzles.puzzle_type_id = puzzle_types.id
                WHERE puzzles.external_id = :external_id"""
            ),
            {"external_id": external_id},
        ).first()
        conn.commit()
        if result is not None:
            puzzle_type = PuzzleType(
                external_id=result.puzzle_types_external_id,
                display_name=result.puzzle_types_display_name,
            )
            return Puzzle(
                puzzle_type=puzzle_type,
                external_id=result.external_id,
                display_name=result.display_name,
                release_date=result.release_date,
                discontinue_date=result.discontinue_date,
            )
        return None


# MAKE USERS CLASS AND METHOD
# MAKE REVIEWS CLASS AND METHOD
