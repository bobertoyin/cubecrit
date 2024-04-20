SELECT
    reviews.created_at,
    reviews.updated_at,
    reviews.rating,
    reviews.content,
    users.wca_id AS users_wca_id,
    users.joined AS users_joined,
    users.first_name AS users_first_name,
    users.last_name AS users_last_name,
    users.profile_picture_url AS users_profile_picture_url,
    puzzles.external_id AS puzzles_external_id,
    puzzle_types.external_id AS puzzle_types_external_id,
    puzzles.display_name AS puzzles_display_name,
    puzzle_types.display_name AS puzzle_types_display_name,
    puzzles.release_date AS puzzles_release_date,
    puzzles.discontinue_date AS puzzles_discontinue_date,
    manufacturers.external_id AS manufacturers_external_id,
    manufacturers.display_name AS manufacturers_display_name,
    countries.external_id AS countries_external_id,
    countries.display_name AS countries_display_name
FROM reviews
INNER JOIN users
    ON reviews.user_id = users.id
INNER JOIN puzzles
    ON reviews.puzzle_id = puzzles.id
INNER JOIN puzzle_types
    ON puzzles.puzzle_type_id = puzzle_types.id
INNER JOIN manufacturers
    ON puzzles.manufacturer_id = manufacturers.id
INNER JOIN countries
    ON manufacturers.country_id = countries.id
WHERE
    users_wca_id = :wca_id
    AND puzzles.external_id = :puzzles_external_id;
