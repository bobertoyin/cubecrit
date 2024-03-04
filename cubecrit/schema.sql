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
