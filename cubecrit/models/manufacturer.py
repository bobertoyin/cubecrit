"""Data models for manufacturers."""
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import Connection, text


@dataclass(frozen=True)
class Country:
    external_id: str
    display_name: str

    @staticmethod
    def get_country(conn: Connection, external_id: str) -> Optional["Country"]:
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
    external_id: str
    display_name: str
    country: Country

    @staticmethod
    def get_manufacturer(
        conn: Connection, external_id: str
    ) -> Optional["Manufacturer"]:
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
