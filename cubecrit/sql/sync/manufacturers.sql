INSERT INTO manufacturer (
    external_id, display_name, country_id, picture_url, bio
)
VALUES (:external_id, :display_name, (
    SELECT country.id AS country_id FROM country
    WHERE country.external_id = country.:country_external_id
), :picture_url, :bio)
ON CONFLICT (external_id) DO UPDATE
SET
external_id = excluded.external_id,
display_name = excluded.display_name,
country_id = excluded.country_id,
picture_url = excluded.picture_url,
bio = excluded.bio;
