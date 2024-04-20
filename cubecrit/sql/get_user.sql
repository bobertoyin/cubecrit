SELECT
    wca_id,
    joined,
    first_name,
    last_name,
    profile_picture_url
FROM "user"
WHERE wca_id = :wca_id;
