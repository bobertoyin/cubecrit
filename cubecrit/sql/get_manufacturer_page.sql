SELECT
    manufacturer.external_id,
    country.external_id AS country_external_id,
    manufacturer.display_name,
    country.display_name AS country_display_name,
    manufacturer.bio
FROM manufacturer
INNER JOIN country ON manufacturer.country_id = country.id
ORDER BY manufacturer.display_name
LIMIT :per_page OFFSET :result_offset;
