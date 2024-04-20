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
                puzzle = Puzzle(
                    result.puzzle_external_id,
                    result.puzzle_display_name,
                    result.puzzle_release_date,
                    result.puzzle_discontinue_date,
                    puzzle_type,
                    manufacturer,
                )
                user = User(
                    result.user_wca_id,
                    result.user_joined,
                    result.user_first_name,
                    result.user_last_name,
                    result.user_profile_picture_url,
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
