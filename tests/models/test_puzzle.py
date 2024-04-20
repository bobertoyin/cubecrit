from datetime import date

from pytest import mark
from sqlalchemy import Connection

from cubecrit.models.manufacturer import Country, Manufacturer
from cubecrit.models.puzzle import Puzzle, PuzzleType


@mark.parametrize(
    "external_id, expected",
    [
        ("3x3", PuzzleType("3x3", "3x3")),
        ("-1x-1", None),
        ("megaminx", PuzzleType("megaminx", "Megaminx")),
        ("Megaminx", None),
    ],
)
def test_get_puzzle_type(
    db_connection: Connection, external_id: str, expected: PuzzleType | None
):
    result = PuzzleType.get_puzzle_type(db_connection, external_id)
    assert result == expected


@mark.parametrize(
    "external_id, expected",
    [
        ("aolong-v3", None),
        ("AOLONG-V2", None),
        (
            "rs3-m-2020",
            Puzzle(
                "rs3-m-2020",
                "RS3 M 2020",
                date(2020, 5, 1),
                date(2020, 5, 1),
                PuzzleType("3x3", "3x3"),
                Manufacturer("moyu", "MoYu", Country("china", "China")),
            ),
        ),
        (
            "aolong-v2",
            Puzzle(
                "aolong-v2",
                "AoLong V2",
                date(2014, 6, 1),
                date(2018, 6, 1),
                PuzzleType("3x3", "3x3"),
                Manufacturer("moyu", "MoYu", Country("china", "China")),
            ),
        ),
        ("RS3 M 2020", None),
    ],
)
def test_get_puzzle(
    db_connection: Connection, external_id: str, expected: Puzzle | None
):
    result = Puzzle.get_puzzle(db_connection, external_id)
    assert result == expected
