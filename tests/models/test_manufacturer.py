from dataclasses import asdict
from unittest.mock import MagicMock, patch

from munch import Munch
from pytest import mark

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
        ("moyu", Manufacturer("moyu", "Moyu", Country("china", "China"),"moyu")),
        ("MOYU", None),
        (
            "rubiks",
            Manufacturer("rubiks", "Rubik's Brand Ltd", Country("canada", "Canada"),"rubik"),
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
            }
        )
    else:
        mock_connection.execute().first.return_value = None

    # act
    result = Manufacturer.get_manufacturer(mock_connection, external_id)

    # assert
    assert result == expected
