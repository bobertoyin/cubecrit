"""Functions for validating user input."""


def validate_page_number(page_number: str | None, num_pages: int) -> int:
    """Validate the user's input for a page number.

    Parameters:
    - page_number: the page number from the URL
    - num_pages: the number of pages available

    Throws an exception if the page_number is larger than the number of pages available or is less than 1.

    Returns the user's page number, or 1 if the page number is not provided or can't be parsed to an integer.
    """
    if page_number is None:
        return 1
    try:
        check_num = int(page_number)
    except ValueError:
        return 1
    if check_num > num_pages or check_num < 1:
        raise ValueError()
    return check_num


def validate_url_param(param: str | None) -> str | None:
    """Validate the URL parameter.

    Parameters:
    - param: the URL parameter

    Returns the URL parameter with whitespace removed, or None if there is nothing in the parameter.
    """
    if param is None:
        return param
    stripped_param = param.strip()
    if stripped_param == "":
        return None
    return stripped_param
