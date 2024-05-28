from io import BytesIO, StringIO
from unittest.mock import MagicMock, call, patch

from pytest import mark

from cubecrit.sync import (
    DATA_URL,
    CSVRow,
    _extract_data,
    _replace_empty_string,
    _sync_data_delegate,
    sync_data,
    sync_data_with_conn,
)


@mark.parametrize(
    "row, expected",
    [
        ({}, {}),
        ({"foo": 12}, {"foo": 12}),
        ({"foo": "bar", "bar": 12}, {"foo": "bar", "bar": 12}),
        ({"foo": None}, {"foo": None}),
        ({"foo": " "}, {"foo": " "}),
        ({"foo": ""}, {"foo": None}),
        ({"foo": "bar", "bar": ""}, {"foo": "bar", "bar": None}),
    ],
)
def test__replace_empty_string(row: CSVRow, expected: CSVRow):
    # act
    result = _replace_empty_string(row)

    # assert
    assert result == expected


@patch("cubecrit.sync.urlopen")
@mark.parametrize(
    "mock_csv, name, expected",
    [
        ("", "empty", []),
        ("h1,h1", "empty_with_headers", []),
        ("h1,h2\nr1c1,r1c2", "one_full_row", [{"h1": "r1c1", "h2": "r1c2"}]),
        (
            "h1,h2\nr1c1,r1c2\nr2c1,r2c2",
            "two_full_row",
            [{"h1": "r1c1", "h2": "r1c2"}, {"h1": "r2c1", "h2": "r2c2"}],
        ),
        (
            "h1,h2\nr1c1,\nr2c1,r2c2",
            "missing_end_cell",
            [{"h1": "r1c1", "h2": None}, {"h1": "r2c1", "h2": "r2c2"}],
        ),
        (
            "h1,h2\n,r1c2\nr2c1,r2c2",
            "missing_start_cell",
            [{"h1": None, "h2": "r1c2"}, {"h1": "r2c1", "h2": "r2c2"}],
        ),
        (
            "h1,h2\n,\nr2c1,r2c2",
            "missing_all_cells",
            [{"h1": None, "h2": None}, {"h1": "r2c1", "h2": "r2c2"}],
        ),
    ],
)
def test__extract_data(
    mock_file: MagicMock, mock_csv: str, name: str, expected: list[CSVRow]
):
    # arrange
    mock_file.return_value = BytesIO(mock_csv.encode())

    # act
    result = _extract_data(name)

    # assert
    mock_file.assert_called_once_with(f"{DATA_URL}/{name}.csv")
    assert result == expected


@patch("builtins.open")
@patch("cubecrit.sync.urlopen")
@patch("sqlalchemy.Connection")
def test__sync_data_delegate(
    mock_connection: MagicMock, mock_file: MagicMock, mock_query_open: MagicMock
):
    # arrange
    mock_query_open.return_value = StringIO("SELECT foo FROM bar;")
    mock_file.return_value = BytesIO("h1,h2\n,\nr2c1,r2c2".encode())

    # act
    _sync_data_delegate(mock_connection, "test")

    # assert
    mock_query_open.assert_called_once_with("cubecrit/sql/sync/test.sql")
    mock_file.assert_called_once_with(f"{DATA_URL}/test.csv")
    mock_connection.execute.assert_called_once_with(
        mock_connection.execute.call_args[0][0],
        [{"h1": None, "h2": None}, {"h1": "r2c1", "h2": "r2c2"}],
    )
    assert (
        str(mock_connection.execute.call_args[0][0].compile()) == "SELECT foo FROM bar;"
    )


@patch("cubecrit.sync._sync_data_delegate")
@patch("sqlalchemy.Connection")
def test_sync_data_with_conn(mock_connection: MagicMock, mock_delegate: MagicMock):
    # act
    sync_data_with_conn(mock_connection)

    # assert
    mock_delegate.assert_has_calls(
        [
            call(mock_connection, "puzzle_types"),
            call(mock_connection, "countries"),
            call(mock_connection, "manufacturers"),
            call(mock_connection, "puzzles"),
        ]
    )
    mock_connection.commit.assert_called_once()


@patch("cubecrit.sync.sync_data_with_conn")
@patch("cubecrit.db.db.connect")
def test_sync_data(mock_connect: MagicMock, mock_sync_with_conn: MagicMock):
    # arrange
    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection

    # act
    sync_data()

    # assert
    mock_connect.assert_called_once()
    mock_sync_with_conn.assert_called_once_with(mock_connection.__enter__())
