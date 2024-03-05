from pytest import mark
from sqlalchemy import Connection

from cubecrit.models.puzzle import PuzzleType


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
