SELECT
    review.created_at,
    review.updated_at,
    review.rating,
    review.content,
    "user".wca_id AS user_wca_id,
    "user".joined AS user_joined,
    "user".first_name AS user_first_name,
    "user".last_name AS user_last_name,
    "user".profile_picture_url AS user_profile_picture_url,
    puzzle.external_id AS puzzle_external_id,
    puzzle_type.external_id AS puzzle_type_external_id,
    puzzle.display_name AS puzzle_display_name,
    puzzle_type.display_name AS puzzle_type_display_name,
    puzzle.release_date AS puzzle_release_date,
    puzzle.discontinue_date AS puzzle_discontinue_date,
    manufacturer.external_id AS manufacturer_external_id,
    manufacturer.display_name AS manufacturer_display_name,
    country.external_id AS country_external_id,
    country.display_name AS country_display_name
FROM review
INNER JOIN "user"
    ON review.user_id = "user".id
INNER JOIN puzzle
    ON review.puzzle_id = puzzle.id
INNER JOIN puzzle_type
    ON puzzle.puzzle_type_id = puzzle_type.id
INNER JOIN manufacturer
    ON puzzle.manufacturer_id = manufacturer.id
INNER JOIN country
    ON manufacturer.country_id = country.id
WHERE
    user_wca_id = :wca_id
    AND puzzle.external_id = :puzzle_external_id;
