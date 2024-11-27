from dataclasses import asdict
from unittest.mock import MagicMock, patch

from munch import Munch
from pytest import mark, raises

from cubecrit.models.manufacturer import Country, Manufacturer


@patch("sqlalchemy.Connection")
@mark.parametrize(
    "external_id, expected",
    [
        ("china", Country("china", "China")),
        ("texas", None),
        ("usa", Country("usa", "United States of America")),
        ("south_pole", None),
    ],
)
def test_get_country(
    mock_connection: MagicMock, external_id: str, expected: Country | None
):
    # arrange
    if expected:
        mock_connection.execute().first()._asdict.return_value = asdict(expected)
    else:
        mock_connection.execute().first.return_value = None

    # act
    result = Country.get_country(mock_connection, external_id)

    # assert
    assert result == expected


@patch("sqlalchemy.Connection")
@mark.parametrize(
    "external_id, expected",
    [
        ("moyu", Manufacturer("moyu", "Moyu", Country("china", "China"), "moyu")),
        ("MOYU", None),
        (
            "rubiks",
            Manufacturer(
                "rubiks", "Rubik's Brand Ltd", Country("canada", "Canada"), "rubik"
            ),
        ),
        ("bruh", None),
    ],
)
def test_get_manufacturer(
    mock_connection: MagicMock, external_id: str, expected: Manufacturer | None
):
    # arrange
    if expected:
        mock_connection.execute().first.return_value = Munch(
            **{
                "country_external_id": expected.country.external_id,
                "country_display_name": expected.country.display_name,
                "external_id": expected.external_id,
                "display_name": expected.display_name,
                "bio": expected.bio,
            }
        )
    else:
        mock_connection.execute().first.return_value = None

    # act
    result = Manufacturer.get_manufacturer(mock_connection, external_id)

    # assert
    assert result == expected


@patch("sqlalchemy.Connection")
@mark.parametrize(
    "page_size, manufacturer_count, expected",
    [
        (1, 1, 1),
        (1, 0, 0),
        (1, 12, 12),
        (2, 12, 6),
        (2, 13, 7),
        (2, 14, 7),
        (3, 19, 7),
        (3, 20, 7),
    ],
)
def test_get_num_pages(
    mock_connection: MagicMock, page_size: int, manufacturer_count: int, expected: int
):
    # arrange
    mock_connection.execute().first.return_value = Munch(
        **{"manufacturer_count": manufacturer_count}
    )

    # act
    result = Manufacturer.get_num_pages(mock_connection, page_size)

    # assert
    assert result == expected


@patch("sqlalchemy.Connection")
@mark.parametrize(
    "page_size, manufacturer_count",
    [
        (0, 12),
        (-1, 1),
        (4, None),
    ],
)
def test_get_num_pages_error(
    mock_connection: MagicMock, page_size: int, manufacturer_count: int | None
):
    # arrange
    if manufacturer_count:
        mock_connection.execute().first.return_value = Munch(
            **{"manufacturer_count": manufacturer_count}
        )
    else:
        mock_connection.execute().first.return_value = None

    # act and assert
    with raises(ValueError):
        result = Manufacturer.get_num_pages(mock_connection, page_size)


@patch("sqlalchemy.Connection")
@mark.parametrize(
    "page_size, page_number, expected",
    [
        (1, 12, []),
        (
            2,
            1,
            [
                Manufacturer(
                    "foo", "foobar", Country("place", "placeland"), "the first foo"
                ),
                Manufacturer(
                    "bar", "barfoo", Country("place", "placeland"), "the first bar"
                ),
            ],
        ),
    ],
)
def test_get_page(
    mock_connection: MagicMock,
    page_size: int,
    page_number: int,
    expected: list[Manufacturer],
):
    # arrange
    mock_connection.execute.return_value = [
        Munch(
            **{
                "external_id": row.external_id,
                "country_external_id": row.country.external_id,
                "display_name": row.display_name,
                "country_display_name": row.country.display_name,
                "bio": row.bio,
            }
        )
        for row in expected
    ]

    # act
    result = Manufacturer.get_page(mock_connection, page_size, page_number)

    # assert
    assert result == expected


@patch("sqlalchemy.Connection")
@mark.parametrize(
    "page_size, page_number",
    [
        (0, 12),
        (-1, 12),
    ],
)
def test_get_page_error(mock_connection: MagicMock, page_size: int, page_number: int):
    # arrange
    mock_connection.execute().first.return_value = None

    # act and assert
    with raises(ValueError):
        result = Manufacturer.get_page(mock_connection, page_size, page_number)
