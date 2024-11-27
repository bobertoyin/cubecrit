"""Data models for manufacturers."""
from dataclasses import dataclass
from math import ceil
from typing import Any, Optional

from sqlalchemy import Connection, Row, text


@dataclass(frozen=True)
class Country:
    """A country."""

    external_id: str
    """The user-facing identifier."""
    display_name: str
    """The formatted display name."""

    @staticmethod
    def get_country(conn: Connection, external_id: str) -> Optional["Country"]:
        """Get a country based on a given external ID.

        Parameters:
        - conn: the database connection
        - external_id: the user-facing identifier

        Returns a country, or None if the external ID does not exist.
        """
        result = conn.execute(
            text(
                "SELECT external_id, display_name FROM country WHERE external_id = :external_id"
            ),
            {"external_id": external_id},
        ).first()
        conn.commit()
        if result is not None:
            return Country(**result._asdict())
        return None


@dataclass(frozen=True)
class Manufacturer:
    """A puzzle manufacturer."""

    external_id: str
    """The user-facing identifier."""
    display_name: str
    """The formatted display name."""
    country: Country
    """The manufacturer's country of origin."""
    bio: str
    """The manufacturer's description."""

    @staticmethod
    def __convert_from_row(row: Row[Any]) -> "Manufacturer":
        """Convert a SQLAlchemy row into a Manufacturer.

        Parameters:
        - row: the row of SQL data

        Returns a manufacturer.
        """
        country = Country(
            row.country_external_id,
            row.country_display_name,
        )
        return Manufacturer(row.external_id, row.display_name, country, row.bio)

    @staticmethod
    def get_manufacturer(
        conn: Connection, external_id: str
    ) -> Optional["Manufacturer"]:
        """Get a manufacturer based on a given external ID.

        Parameters:
        - conn: the database connection
        - external_id: the user-facing identifier

        Returns a manufacturer, or None if the external ID does not exist.
        """
        with open("cubecrit/sql/get_manufacturer.sql") as query:
            result = conn.execute(
                text(query.read()),
                {"external_id": external_id},
            ).first()
            conn.commit()
            if result is not None:
                return Manufacturer.__convert_from_row(result)
            return None

    @staticmethod
    def get_num_pages(
        conn: Connection,
        page_size: int,
    ) -> int:
        """Get the total number of pages of manufacturers currently in the database.

        Parameters:
        - page_size: the maximum number of manufacturers per page

        Raises:
        - a ValueError if page_size is less than 1
        - an ValueError if the SQL query fails to return anything

        Returns the total number of pages.
        """
        if page_size < 1:
            raise ValueError(page_size)
        with open("cubecrit/sql/get_num_manufacturers.sql") as query:
            result = conn.execute(text(query.read())).first()
            conn.commit()
            if result is None:
                raise ValueError(result)
            return ceil(result.manufacturer_count / page_size)

    @staticmethod
    def get_page(
        conn: Connection,
        page_size: int,
        page_number: int,
    ) -> list["Manufacturer"]:
        """Get a paginated list of manufacturers.

        The manufacturers are sorted by name in lexicographical order.

        Parameters:
        - conn: the database connection
        - page_size: the maximum number of manufacturers per page
        - page_number: the page number to retrieve

        Raises:
        - a ValueError if page_size is less than 1

        Returns a list of manufacturers for the page.
        """
        if page_size < 1:
            raise ValueError(page_size)
        with open("cubecrit/sql/get_manufacturer_page.sql") as query:
            result = conn.execute(
                text(query.read()),
                {
                    "per_page": page_size,
                    "result_offset": (page_number - 1) * page_size,
                },
            )
            conn.commit()
            return [Manufacturer.__convert_from_row(row) for row in result]
