CREATE TABLE IF NOT EXISTS puzzle_types (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS manufacturers (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL,
    country_id INT UNIQUE NOT NULL,
    -- picture TEXT
    CONSTRAINT fk_country
        FOREIGN KEY (country_id)
        REFERENCES countries(id)
);

CREATE TABLE IF NOT EXISTS puzzles (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL,
    release_date DATE,
    discontinue_date DATE,
    puzzle_type_id INT NOT NULL,
    manufacturer_id INT NOT NULL,
    -- picture TEXT,
    CONSTRAINT fk_puzzle_type
        FOREIGN KEY(puzzle_type_id)
        REFERENCES puzzle_types(id),
    CONSTRAINT fk_manufacturer
        FOREIGN KEY(manufacturer_id)
        REFERENCES manufacturers(id)
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    wca_id VARCHAR UNIQUE NOT NULL,
    joined TIMESTAMP DEFAULT NOW(),
    first_name VARCHAR,
    last_name VARCHAR
    -- profile_picture TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    puzzle_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    rating INT NOT NULL,
    content TEXT,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id),
    CONSTRAINT fk_puzzle
        FOREIGN KEY (puzzle_id)
        REFERENCES puzzles(id)
);

INSERT INTO countries(external_id, display_name)
VALUES ('china', 'China')
ON CONFLICT(external_id)
DO UPDATE SET
    external_id = EXCLUDED.external_id;

INSERT INTO manufacturers(external_id, display_name, country_id)
VALUES ('moyu', 'MoYu', (SELECT id FROM countries
    WHERE countries.external_id = 'china'))
ON CONFLICT(external_id)
DO UPDATE SET
    external_id = EXCLUDED.external_id;

INSERT INTO puzzle_types(external_id, display_name)
VALUES ('3x3', '3x3')
ON CONFLICT(external_id)
DO UPDATE SET
    external_id = EXCLUDED.external_id;

INSERT INTO puzzles(external_id, display_name, release_date, discontinue_date, puzzle_type_id, manufacturer_id)
VALUES ('aolong-v2', 'AoLong V2', '2014-06-01', '2018-06-01', 
    (SELECT id FROM puzzle_types
        WHERE puzzle_types.external_id = '3x3'), 
    (SELECT id FROM manufacturers
        WHERE manufacturers.external_id = 'moyu'))
ON CONFLICT(external_id)
DO UPDATE SET
    external_id = EXCLUDED.external_id;