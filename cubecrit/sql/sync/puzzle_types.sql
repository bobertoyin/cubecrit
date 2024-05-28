INSERT INTO puzzle_type (external_id, display_name)
VALUES (:external_id, :display_name)
ON CONFLICT (external_id) DO UPDATE
SET
external_id = excluded.external_id,
display_name = excluded.display_name;
