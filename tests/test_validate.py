from pytest import mark, raises

from cubecrit.validate import validate_page_number, validate_url_param


@mark.parametrize(
    "page_number, num_pages, expected",
    [
        ("", 1, 1),
        ("2", 2, 2),
        ("10", 10, 10),
        ("abcd", 1, 1),
        (None, 1, 1),
    ],
)
def test_validate_page_number(page_number: str | None, num_pages: int, expected: int):
    result = validate_page_number(page_number, num_pages)
    assert result == expected


@mark.parametrize("page_number, num_pages", [("2", 1), ("-1", 1), ("0", 1)])
def test_validate_page_number_error(page_number: str | None, num_pages: int):
    with raises(ValueError):
        validate_page_number(page_number, num_pages)


@mark.parametrize(
    "param, expected",
    [
        ("  aolong ", "aolong"),
        ("aolong", "aolong"),
        (None, None),
        ("", None),
        ("   ", None),
    ],
)
def test_validate_url_param(param: str | None, expected: str | None):
    result = validate_url_param(param)
    assert result == expected
