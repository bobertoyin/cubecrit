SELECT
    manufacturer.external_id,
    country.external_id AS country_external_id,
    manufacturer.display_name,
    country.display_name AS country_display_name,
    manufacturer.bio
FROM manufacturer
INNER JOIN country ON manufacturer.country_id = country.id
WHERE manufacturer.external_id = :external_id;
