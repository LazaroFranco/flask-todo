DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS items;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE items (
  id bigserial  PRIMARY KEY,
  task text NOT NULL,
  task_timestamp timestamp NOT NULL,
  completed boolean NOT NULL
);
