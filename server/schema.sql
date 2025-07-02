-- Database schema for character customization project

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  point_balance INTEGER NOT NULL DEFAULT 1000
);

CREATE TABLE IF NOT EXISTS characters (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  intro TEXT
);

CREATE TABLE IF NOT EXISTS user_characters (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  character_id INTEGER NOT NULL REFERENCES characters(id)
);

CREATE TABLE IF NOT EXISTS packages (
  id SERIAL PRIMARY KEY,
  character_id INTEGER NOT NULL REFERENCES characters(id),
  name VARCHAR(150) NOT NULL,
  thumbnail_url VARCHAR(500) NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS patch_groups (
  id SERIAL PRIMARY KEY,
  character_id INTEGER NOT NULL REFERENCES characters(id),
  name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  package_id INTEGER NOT NULL REFERENCES packages(id),
  patch_group_id INTEGER NOT NULL REFERENCES patch_groups(id),
  name VARCHAR(100) NOT NULL,
  price INTEGER NOT NULL DEFAULT 10,
  metadata JSONB,
  original_image_url VARCHAR(500) NOT NULL,
  web_image_url VARCHAR(500) NOT NULL,
  is_default BOOLEAN NOT NULL DEFAULT FALSE,
  UNIQUE(package_id, patch_group_id) WHERE is_default = TRUE
);

CREATE TABLE IF NOT EXISTS user_items (
  user_id INTEGER NOT NULL REFERENCES users(id),
  item_id INTEGER NOT NULL REFERENCES items(id),
  PRIMARY KEY(user_id, item_id)
);

CREATE TABLE IF NOT EXISTS user_character_customizations (
  user_character_id INTEGER NOT NULL REFERENCES user_characters(id),
  patch_group_id INTEGER NOT NULL REFERENCES patch_groups(id),
  item_id INTEGER NOT NULL REFERENCES items(id),
  PRIMARY KEY(user_character_id, patch_group_id),
  FOREIGN KEY(patch_group_id, item_id) REFERENCES items(patch_group_id, id)
);
