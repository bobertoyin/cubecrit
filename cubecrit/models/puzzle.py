from dataclasses import dataclass
from datetime import date
from sqlalchemy import Connection, text


@dataclass(frozen=True)
class PuzzleType:
    external_id: str
    display_name: str


@dataclass(frozen=True)
class Puzzle:
    external_id: str
    display_name: str
    release_date: date | None
    discontinue_date: date | None
    puzzle_type: PuzzleType


def get_puzzle_type(conn: Connection, external_id: str) -> PuzzleType | None:
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


def get_puzzle_type_internal(conn: Connection, internal_id: int) -> PuzzleType | None:
    result = conn.execute(
        text(
            "SELECT external_id, display_name FROM puzzle_types WHERE id = :internal_id"
        ),
        {"internal_id": internal_id},
    ).first()
    conn.commit()
    if result is not None:
        return PuzzleType(**result._asdict())
    return None


def get_puzzle(conn: Connection, external_id: str) -> Puzzle | None:
    result = conn.execute(
        text(
            "SELECT external_id, display_name, release_date, discontinue_date, puzzle_type_id FROM puzzles WHERE external_id = :external_id"
        ),
        {"external_id": external_id},
    ).first()
    conn.commit()
    if result is not None:
        puzzle_type = get_puzzle_type_internal(conn, result.puzzle_type_id)
        if puzzle_type is not None:
            return Puzzle(
                puzzle_type=puzzle_type,
                external_id=result.external_id,
                display_name=result.display_name,
                release_date=result.release_date,
                discontinue_date=result.discontinue_date,
            )
    return None
