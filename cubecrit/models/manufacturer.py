"""Data models for manufacturers."""
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Connection, text


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
        result = conn.execute(
            text(
                """SELECT manufacturer.external_id, country.external_id as country_external_id,
                    manufacturer.display_name, country.display_name as country_display_name
                    FROM manufacturer
                    JOIN country ON manufacturer.country_id = country.id
                    WHERE manufacturer.external_id = :external_id
                    """
            ),
            {"external_id": external_id},
        ).first()
        conn.commit()
        if result is not None:
            country = Country(
                result.country_external_id,
                result.country_display_name,
            )
            return Manufacturer(
                result.external_id,
                result.display_name,
                country,
            )
        return None
