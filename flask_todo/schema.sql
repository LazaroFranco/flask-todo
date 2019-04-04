DROP TABLE IF EXISTS items;

CREATE TABLE items (
  id bigserial  PRIMARY KEY,
  task text NOT NULL,
  task_timestamp timestamp NOT NULL,
  completed boolean NOT NULL
);
