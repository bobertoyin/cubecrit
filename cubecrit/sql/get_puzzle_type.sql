SELECT
    external_id,
    display_name
FROM puzzle_types
WHERE external_id = :external_id;
