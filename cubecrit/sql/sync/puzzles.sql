INSERT INTO puzzle (
    external_id,
    display_name,
    puzzle_type_id,
    manufacturer_id,
    release_date,
    discontinue_date,
    picture_url
)
VALUES (
    :external_id,
    :display_name,
    (
        SELECT puzzle_type.id AS puzzle_type_id
        FROM puzzle_type
        WHERE puzzle_type.external_id = :puzzle_type_external_id
    ),
    (
        SELECT manufacturer.id AS manufacturer_id
        FROM manufacturer
        WHERE manufacturer.external_id = :manufacturer_external_id
    ),
    :release_date,
    :discontinue_date,
    :picture_url
)
ON CONFLICT (external_id) DO UPDATE
SET
external_id = excluded.external_id,
display_name = excluded.display_name,
puzzle_type_id = excluded.puzzle_type_id,
manufacturer_id = excluded.manufacturer_id,
release_date = excluded.release_date,
discontinue_date = excluded.discontinue_date,
picture_url = excluded.picture_url;
