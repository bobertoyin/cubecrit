"""Functions for validating user input."""
def validate_page_number(page_number: str | None) -> int:
    """Validate the user's input for a page number.

    Parameters:
    - page_number: the page number from the URL

    Returns the user's page number, or 1 if the page number is not provided or can't be parsed to an integer.
    """
    if page_number is None:
        return 1
    try:
        check_num = int(page_number)
        return check_num
    except ValueError:
        return 1


def validate_query(query: str | None) -> str | None:
    """Validate the user's input for query.

    Parameters:
    - query: the user's input from the URL

    Returns the user's query with whitespace removed, or None if there is nothing in the query.
    """
    if query is None:
        return query
    stripped_query = query.strip()
    if stripped_query == "":
        return None
    return stripped_query
