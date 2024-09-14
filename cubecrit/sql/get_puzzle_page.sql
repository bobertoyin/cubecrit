SELECT
    puzzle.external_id,
    puzzle_type.external_id AS puzzle_type_external_id,
    puzzle.display_name,
    puzzle_type.display_name AS puzzle_type_display_name,
    puzzle.release_date,
    puzzle.discontinue_date,
    manufacturer.external_id AS manufacturer_external_id,
    manufacturer.display_name AS manufacturer_display_name,
    country.external_id AS country_external_id,
    country.display_name AS country_display_name
FROM puzzle
INNER JOIN puzzle_type
    ON puzzle.puzzle_type_id = puzzle_type.id
INNER JOIN manufacturer
    ON puzzle.manufacturer_id = manufacturer.id
INNER JOIN country
    ON manufacturer.country_id = country.id
WHERE
    (:puzzle_type IS NULL OR puzzle_type.external_id = :puzzle_type)
    AND (:q IS NULL OR LOWER(puzzle.display_name) LIKE CONCAT('%', :q, '%'))
ORDER BY manufacturer.display_name, puzzle.display_name
LIMIT :puzzles_per_page OFFSET :puzzles_offset;
