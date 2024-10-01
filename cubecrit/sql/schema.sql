CREATE TABLE IF NOT EXISTS puzzle_type (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS country (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS manufacturer (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL,
    country_id INT NOT NULL,
    picture_url VARCHAR,
    bio VARCHAR,
    CONSTRAINT fk_country
    FOREIGN KEY (country_id)
    REFERENCES country (id)
);

CREATE TABLE IF NOT EXISTS puzzle (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR UNIQUE NOT NULL,
    display_name VARCHAR NOT NULL,
    release_date DATE,
    discontinue_date DATE,
    puzzle_type_id INT NOT NULL,
    manufacturer_id INT NOT NULL,
    picture_url VARCHAR,
    CONSTRAINT fk_puzzle_type
    FOREIGN KEY (puzzle_type_id)
    REFERENCES puzzle_type (id),
    CONSTRAINT fk_manufacturer
    FOREIGN KEY (manufacturer_id)
    REFERENCES manufacturer (id)
);

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    wca_id VARCHAR UNIQUE NOT NULL,
    joined TIMESTAMP DEFAULT NOW(),
    first_name VARCHAR,
    last_name VARCHAR,
    profile_picture_url VARCHAR
);

CREATE TABLE IF NOT EXISTS review (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    puzzle_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    rating INT NOT NULL,
    content TEXT,
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES "user" (id),
    CONSTRAINT fk_puzzle
    FOREIGN KEY (puzzle_id)
    REFERENCES puzzle (id),
    UNIQUE (user_id, puzzle_id)
);
