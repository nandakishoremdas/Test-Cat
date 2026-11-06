-- Cat Registration: schema "cat", table "family"
CREATE SCHEMA IF NOT EXISTS cat;

CREATE TABLE IF NOT EXISTS cat.family (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    breed       VARCHAR(100),
    age         INTEGER CHECK (age >= 0),
    gender      VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
    color       VARCHAR(50),
    owner_name  VARCHAR(100) NOT NULL,
    owner_phone VARCHAR(20),
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);