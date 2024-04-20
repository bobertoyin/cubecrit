from datetime import date
from unittest.mock import MagicMock, patch

from munch import Munch
from pytest import mark

from cubecrit.models.manufacturer import Country, Manufacturer
from cubecrit.models.puzzle import Puzzle, PuzzleType


@patch("sqlalchemy.Connection")
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
    mock_connection: MagicMock, external_id: str, expected: PuzzleType | None
):
    # arrange
    if expected:
        mock_connection.execute().first()._asdict.return_value = {
            "external_id": expected.external_id,
            "display_name": expected.display_name,
        }
    else:
        mock_connection.execute().first.return_value = None

    # act
    result = PuzzleType.get_puzzle_type(mock_connection, external_id)

    # assert
    assert result == expected


@patch("sqlalchemy.Connection")
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
    mock_connection: MagicMock, external_id: str, expected: Puzzle | None
):
    # arrange
    if expected:
        mock_return: Munch = Munch(
            **{
                "external_id": expected.external_id,
                "display_name": expected.display_name,
                "release_date": expected.release_date,
                "discontinue_date": expected.discontinue_date,
                "puzzle_type_external_id": expected.puzzle_type.external_id,
                "puzzle_type_display_name": expected.puzzle_type.display_name,
                "manufacturer_external_id": expected.manufacturer.external_id,
                "manufacturer_display_name": expected.manufacturer.display_name,
                "country_external_id": expected.manufacturer.country.external_id,
                "country_display_name": expected.manufacturer.country.display_name,
            }
        )
        mock_connection.execute().first.return_value = mock_return
    else:
        mock_connection.execute().first.return_value = None

    # act
    result = Puzzle.get_puzzle(mock_connection, external_id)

    # assert
    assert result == expected
