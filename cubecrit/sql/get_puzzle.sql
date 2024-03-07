SELECT
    puzzles.external_id,
    puzzle_types.external_id AS puzzle_types_external_id,
    puzzles.display_name,
    puzzle_types.display_name AS puzzle_types_display_name,
    puzzles.release_date,
    puzzles.discontinue_date,
    manufacturers.external_id AS manufacturers_external_id,
    manufacturers.display_name AS manufacturers_display_name,
    countries.external_id AS countries_external_id,
    countries.display_name AS countries_display_name
FROM puzzles
INNER JOIN puzzle_types
    ON puzzles.puzzle_type_id = puzzle_types.id
INNER JOIN manufacturers
    ON puzzles.manufacturer_id = manufacturers.id
INNER JOIN countries
    ON manufacturers.country_id = countries.id
WHERE puzzles.external_id = :external_id
