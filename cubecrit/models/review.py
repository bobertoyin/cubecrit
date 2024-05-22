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
    """A user-submitted puzzle review."""

    user: User
    """The user who wrote the review."""
    puzzle: Puzzle
    """The puzzle that is being reviewed."""
    created_at: datetime
    """When the review was created."""
    updated_at: datetime | None
    """When the review was last updated."""
    rating: int
    """The rating associated with the review."""
    content: str | None
    """The contents of the review."""

    @staticmethod
    def get_review(
        conn: Connection, wca_id: str, puzzle_external_id: str
    ) -> Optional["Review"]:
        """Get a review for a cube by a user.

        Parameters:
        - conn: the database connection
        - wca_id: the user's WCA ID
        - puzzle_external_id: The puzzle's external ID

        Returns a review, or None if the user hasn't reviewed the cube.
        """
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
