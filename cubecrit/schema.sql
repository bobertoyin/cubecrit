CREATE TABLE IF NOT EXISTS greetings (
    id SERIAL PRIMARY KEY,
    greeting VARCHAR UNIQUE NOT NULL
);

INSERT INTO greetings(greeting)
VALUES ('hello')
ON CONFLICT(greeting)
DO UPDATE SET
    greeting = EXCLUDED.greeting;

INSERT INTO greetings(greeting)
VALUES ('salutations')
ON CONFLICT(greeting)
DO UPDATE SET
    greeting = EXCLUDED.greeting;

INSERT INTO greetings(greeting)
VALUES ('what''s up')
ON CONFLICT(greeting)
DO UPDATE SET
    greeting = EXCLUDED.greeting;