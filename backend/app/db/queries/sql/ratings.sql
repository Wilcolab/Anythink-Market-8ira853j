-- name: create-ratings-table
CREATE TABLE IF NOT EXISTS ratings (
    id SERIAL PRIMARY KEY,
    value INTEGER NOT NULL,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    comment TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_user_item_rating UNIQUE(item_id, user_id)
);

-- name: create-new-rating
INSERT INTO ratings (value, item_id, user_id, comment)
VALUES (
    :value,
    (SELECT id FROM items WHERE slug = :item_slug),
    (SELECT id FROM users WHERE username = :user_username),
    :comment
)
RETURNING
    id,
    value,
    (SELECT slug FROM items WHERE id = item_id) as item_slug,
    user_id,
    (SELECT username FROM users WHERE id = user_id) as user_username,
    comment,
    created_at,
    updated_at;

-- name: get-rating-by-id-and-slug
SELECT
    r.id,
    r.value,
    i.slug as item_slug,
    r.user_id,
    u.username as user_username,
    r.comment,
    r.created_at,
    r.updated_at
FROM ratings r
JOIN items i ON r.item_id = i.id
JOIN users u ON r.user_id = u.id
WHERE r.id = :rating_id AND i.slug = :item_slug;

-- name: get-ratings-for-item-by-slug
SELECT
    r.id,
    r.value,
    i.slug as item_slug,
    r.user_id,
    u.username as user_username,
    r.comment,
    r.created_at,
    r.updated_at
FROM ratings r
JOIN items i ON r.item_id = i.id
JOIN users u ON r.user_id = u.id
WHERE i.slug = :slug
ORDER BY r.created_at DESC;

-- name: get-user-rating-for-item
SELECT
    r.id,
    r.value,
    i.slug as item_slug,
    r.user_id,
    u.username as user_username,
    r.comment,
    r.created_at,
    r.updated_at
FROM ratings r
JOIN items i ON r.item_id = i.id
JOIN users u ON r.user_id = u.id
WHERE i.slug = :item_slug AND u.username = :user_username;

-- name: update-rating
UPDATE ratings
SET value = :value, comment = :comment, updated_at = NOW()
WHERE id = :rating_id AND user_id = (SELECT id FROM users WHERE username = :user_username)
RETURNING
    id,
    value,
    (SELECT slug FROM items WHERE id = item_id) as item_slug,
    user_id,
    (SELECT username FROM users WHERE id = user_id) as user_username,
    comment,
    created_at,
    updated_at;

-- name: delete-rating-by-id
DELETE FROM ratings
WHERE id = :rating_id AND user_id = (SELECT id FROM users WHERE username = :user_username);

-- name: update-item-rating-stats
WITH rating_stats AS (
    SELECT 
        AVG(r.value) as avg_rating,
        COUNT(r.id) as rating_count
    FROM ratings r
    JOIN items i ON r.item_id = i.id
    WHERE i.slug = :item_slug
)
UPDATE items
SET 
    average_rating = rating_stats.avg_rating,
    ratings_count = rating_stats.rating_count
FROM rating_stats
WHERE slug = :item_slug;

-- name: alter-items-add-rating-columns
ALTER TABLE items
ADD COLUMN IF NOT EXISTS average_rating FLOAT,
ADD COLUMN IF NOT EXISTS ratings_count INTEGER NOT NULL DEFAULT 0;
