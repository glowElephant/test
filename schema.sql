-- SQL schema implementing db.md

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    point_balance INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    intro TEXT
);

CREATE TABLE user_characters (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    character_id INTEGER NOT NULL REFERENCES characters(id)
);

CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters(id),
    name VARCHAR(150) NOT NULL,
    thumbnail_url VARCHAR(500) NOT NULL,
    description TEXT
);

CREATE TABLE patch_groups (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters(id),
    name VARCHAR(50) NOT NULL
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    package_id INTEGER NOT NULL REFERENCES packages(id),
    patch_group_id INTEGER NOT NULL REFERENCES patch_groups(id),
    name VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL DEFAULT 50,
    metadata JSON,
    original_image_url VARCHAR(500) NOT NULL,
    web_image_url VARCHAR(500) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (package_id, patch_group_id, is_default)
);

CREATE TABLE user_character_customizations (
    user_character_id INTEGER NOT NULL REFERENCES user_characters(id),
    patch_group_id INTEGER NOT NULL REFERENCES patch_groups(id),
    item_id INTEGER NOT NULL REFERENCES items(id),
    PRIMARY KEY (user_character_id, patch_group_id),
    FOREIGN KEY (patch_group_id, item_id) REFERENCES items(patch_group_id, id)
);
