CREATE TABLE IF NOT EXISTS puzzle_types (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS puzzles (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL,
    release_date DATE,
    discontinue_date DATE,
    puzzle_type_id INT NOT NULL,
    -- picture TEXT,
    CONSTRAINT fk_puzzle_type
        FOREIGN KEY(puzzle_type_id)
        REFERENCES puzzle_types(id)
);

INSERT INTO puzzle_types(external_id, display_name)
VALUES ('3x3', '3x3')
ON CONFLICT(external_id)
DO UPDATE SET
    external_id = EXCLUDED.external_id;

INSERT INTO puzzles(external_id, display_name, release_date, discontinue_date, puzzle_type_id)
VALUES ('aolong-v2', 'AoLong V2', '2014-06-01', '2018-06-01', (SELECT id from puzzle_types
    WHERE puzzle_types.external_id = '3x3'))
ON CONFLICT(external_id)
DO UPDATE SET
    external_id = EXCLUDED.external_id;