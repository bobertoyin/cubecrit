SELECT COUNT(*) AS num_puzzles FROM puzzle
INNER JOIN puzzle_type
    ON puzzle.puzzle_type_id = puzzle_type.id
WHERE
    (:puzzle_type IS NULL OR puzzle_type.external_id = :puzzle_type)
    AND (:q IS NULL OR LOWER(puzzle.display_name) LIKE CONCAT('%', :q, '%'));
