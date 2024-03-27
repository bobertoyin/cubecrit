INSERT INTO countries (external_id, display_name)
VALUES ('china', 'China')
ON CONFLICT (external_id)
DO UPDATE SET
external_id = excluded.external_id;

INSERT INTO manufacturers (external_id, display_name, country_id)
VALUES ('moyu', 'MoYu', (
    SELECT countries.id FROM countries
    WHERE countries.external_id = 'china'
))
ON CONFLICT (external_id)
DO UPDATE SET
external_id = excluded.external_id;

INSERT INTO puzzle_types (external_id, display_name)
VALUES ('3x3', '3x3')
ON CONFLICT (external_id)
DO UPDATE SET
external_id = excluded.external_id;

INSERT INTO puzzle_types (external_id, display_name)
VALUES ('megaminx', 'Megaminx')
ON CONFLICT (external_id)
DO UPDATE SET
external_id = excluded.external_id;

INSERT INTO users (wca_id, joined, first_name, last_name)
VALUES ('2016PARK02', '2024-03-26', 'Steve', 'Jobs')
ON CONFLICT (wca_id)
DO UPDATE SET
wca_id = excluded.wca_id;

INSERT INTO puzzles (
    external_id,
    display_name,
    release_date,
    discontinue_date,
    puzzle_type_id,
    manufacturer_id
)
VALUES (
    'aolong-v2', 'AoLong V2', '2014-06-01', '2018-06-01',
    (
        SELECT puzzle_types.id FROM puzzle_types
        WHERE puzzle_types.external_id = '3x3'
    ),
    (
        SELECT manufacturers.id FROM manufacturers
        WHERE manufacturers.external_id = 'moyu'
    )
)
ON CONFLICT (external_id)
DO UPDATE SET
external_id = excluded.external_id;

INSERT INTO puzzles (
    external_id,
    display_name,
    release_date,
    discontinue_date,
    puzzle_type_id,
    manufacturer_id
)
VALUES (
    'rs3-m-2020', 'RS3 M 2020', '2020-05-01', '2020-05-01',
    (
        SELECT puzzle_types.id FROM puzzle_types
        WHERE puzzle_types.external_id = '3x3'
    ),
    (
        SELECT manufacturers.id FROM manufacturers
        WHERE manufacturers.external_id = 'moyu'
    )
)
ON CONFLICT (external_id)
DO UPDATE SET
external_id = excluded.external_id;
