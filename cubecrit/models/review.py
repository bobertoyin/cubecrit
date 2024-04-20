"""Data models for reviews."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import Connection, text

from .manufacturer import Country, Manufacturer
from .puzzle import Puzzle, PuzzleType
from .user import User


@dataclass(frozen=True)
class Review:
    user: User
    puzzle: Puzzle
    created_at: datetime
    updated_at: datetime | None
    rating: int
    content: str | None

    @staticmethod
    def get_review(
        conn: Connection, wca_id: str, puzzle_external_id: str
    ) -> Optional["Review"]:
        with open("cubecrit/sql/get_review.sql") as query:
            result = conn.execute(
                text(query.read()),
                {"wca_id": wca_id, "puzzle_external_id": puzzle_external_id},
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
                puzzle = Puzzle(
                    result.puzzles_external_id,
                    result.puzzles_display_name,
                    result.puzzles_release_date,
                    result.puzzles_discontinue_date,
                    puzzle_type,
                    manufacturer,
                )
                user = User(
                    result.users_wca_id,
                    result.users_joined,
                    result.users_first_name,
                    result.users_last_name,
                    result.users_profile_picture_url,
                )
                return Review(
                    user,
                    puzzle,
                    result.created_at,
                    result.updated_at,
                    result.rating,
                    result.content,
                )
            return None
