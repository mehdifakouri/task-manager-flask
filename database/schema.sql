-- Task mangar database schema
-- PostgreSQL 15

CREATE TABLE IF NOT EXISTS tasks(
    id        SERIAL PRIMARY KEY,
    title     VARCHAR(255) NOT NULL,
    description    TEXT,
    completed  BOOLEAN NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
