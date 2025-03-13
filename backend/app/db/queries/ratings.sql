-- name: create_new_rating
INSERT INTO ratings (value, item_id, user_id, comment)
VALUES (:value, :item_id, :user_id, :comment)
RETURNING 
    id, 
    value, 
    item_id,
    user_id,
    comment,
    created_at,
    updated_at;

-- name: get_rating_by_id_and_slug
SELECT r.* 
FROM ratings r
JOIN items i ON r.item_id = i.id
WHERE r.id = :rating_id AND i.slug = :item_slug;

-- name: get_ratings_for_item_by_slug
SELECT r.* 
FROM ratings r
JOIN items i ON r.item_id = i.id
WHERE i.slug = :slug
ORDER BY r.created_at DESC;

-- name: get_average_rating_for_item
SELECT AVG(r.value) as average_rating
FROM ratings r
JOIN items i ON r.item_id = i.id
WHERE i.slug = :item_slug;

-- name: get_user_rating_for_item
SELECT r.* 
FROM ratings r
JOIN items i ON r.item_id = i.id
JOIN users u ON r.user_id = u.id
WHERE i.slug = :item_slug AND u.username = :user_username;

-- name: update_rating
UPDATE ratings r
SET value = :value, comment = :comment, updated_at = NOW()
FROM users u
WHERE r.id = :rating_id 
AND r.user_id = u.id 
AND u.username = :user_username
RETURNING r.*;

-- name: delete_rating_by_id
DELETE FROM ratings r
USING users u
WHERE r.id = :rating_id 
AND r.user_id = u.id 
AND u.username = :user_username;

-- name: decrement_ratings_count
UPDATE items
SET ratings_count = ratings_count - 1
WHERE slug = :item_slug;

-- name: update_item_average_rating
UPDATE items i
SET average_rating = (
  SELECT AVG(value) FROM ratings r WHERE r.item_id = i.id
)
WHERE i.slug = :item_slug;

-- name: increment_ratings_count
UPDATE items
SET ratings_count = ratings_count + 1
WHERE slug = :item_slug;
