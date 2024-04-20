INSERT INTO country (external_id, display_name)
VALUES ('china', 'China')
ON CONFLICT DO NOTHING;

INSERT INTO manufacturer (external_id, display_name, country_id)
VALUES ('moyu', 'MoYu', (
    SELECT country.id FROM country
    WHERE country.external_id = 'china'
))
ON CONFLICT DO NOTHING;

INSERT INTO puzzle_type (external_id, display_name)
VALUES ('3x3', '3x3')
ON CONFLICT DO NOTHING;

INSERT INTO puzzle_type (external_id, display_name)
VALUES ('megaminx', 'Megaminx')
ON CONFLICT DO NOTHING;

INSERT INTO "user" (wca_id, joined, first_name, last_name)
VALUES ('2016PARK02', '2024-03-26', 'Steve', 'Jobs')
ON CONFLICT DO NOTHING;

INSERT INTO puzzle (
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
        SELECT puzzle_type.id FROM puzzle_type
        WHERE puzzle_type.external_id = '3x3'
    ),
    (
        SELECT manufacturer.id FROM manufacturer
        WHERE manufacturer.external_id = 'moyu'
    )
)
ON CONFLICT DO NOTHING;

INSERT INTO puzzle (
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
        SELECT puzzle_type.id FROM puzzle_type
        WHERE puzzle_type.external_id = '3x3'
    ),
    (
        SELECT manufacturer.id FROM manufacturer
        WHERE manufacturer.external_id = 'moyu'
    )
)
ON CONFLICT DO NOTHING;
