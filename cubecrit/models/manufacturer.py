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
                "SELECT external_id, display_name FROM countries WHERE external_id = :external_id"
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
                """SELECT manufacturers.external_id, countries.external_id as countries_external_id,
                    manufacturers.display_name, countries.display_name as countries_display_name
                    FROM manufacturers
                    JOIN countries ON manufacturers.country_id = countries.id
                    WHERE manufacturers.external_id = :external_id
                    """
            ),
            {"external_id": external_id},
        ).first()
        conn.commit()
        if result is not None:
            country = Country(
                result.countries_external_id,
                result.countries_display_name,
            )
            return Manufacturer(
                result.external_id,
                result.display_name,
                country,
            )
        return None
