SELECT
    external_id,
    display_name
FROM puzzle_type
WHERE external_id = :external_id;
