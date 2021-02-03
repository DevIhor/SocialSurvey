-- name: get-user-by-email^
SELECT id, username, email, salt, hashed_password, bio, image, created_at, updated_at
FROM users WHERE email = :email LIMIT 1;

--