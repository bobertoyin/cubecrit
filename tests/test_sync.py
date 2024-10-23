from io import BytesIO, StringIO
from unittest.mock import MagicMock, call, patch

from flask import Flask
from pytest import mark

from cubecrit.sync import (
    CSVRow,
    _extract_data,
    _replace_empty_string,
    _sync_data_delegate,
    scheduler,
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


@patch("builtins.open")
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
    mock_file.return_value = StringIO(mock_csv)

    # act
    result = _extract_data(name)

    # assert
    mock_file.assert_called_once_with(f"cubecrit/data/{name}.csv")
    assert result == expected


@patch("builtins.open")
@patch("sqlalchemy.Connection")
def test__sync_data_delegate(
    mock_connection: MagicMock,
    mock_file: MagicMock,
):
    # arrange
    mock_file.side_effect = [
        StringIO("h1,h2\n,\nr2c1,r2c2"),
        StringIO("SELECT foo FROM bar;"),
    ]

    # act
    _sync_data_delegate(mock_connection, "test")

    # assert
    mock_file.assert_has_calls(
        [call("cubecrit/data/test.csv"), call("cubecrit/sql/sync/test.sql")]
    )
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
def test_sync_data(mock_sync_with_conn: MagicMock):
    # arrange
    mock_engine = MagicMock()
    app = Flask(__name__)
    app.config["db"] = mock_engine
    scheduler.init_app(app)

    # act
    sync_data()

    # assert
    mock_sync_with_conn.assert_called_once_with(mock_engine.connect().__enter__())
