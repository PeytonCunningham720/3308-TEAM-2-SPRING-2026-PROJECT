-- Cawler ID Database Schema
-- PostgreSQL

-- Drop tables in reverse dependency order for clean re-runs
DROP TABLE IF EXISTS identification_history;
DROP TABLE IF EXISTS bird_species;
DROP TABLE IF EXISTS users;

-- 1) Users
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(64)  UNIQUE NOT NULL,
    email         VARCHAR(256) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- 2) Bird Species (reference / field-guide data)
CREATE TABLE bird_species (
    id              SERIAL PRIMARY KEY,
    common_name     VARCHAR(128) NOT NULL,
    scientific_name VARCHAR(128) UNIQUE,
    description     TEXT         NOT NULL,
    ref_audio_path  VARCHAR(512) NOT NULL,
    ref_spec_path   VARCHAR(512) NOT NULL,
    ref_image       VARCHAR(512) NOT NULL
);

-- 3) Identification History
CREATE TABLE identification_history (
    id               SERIAL PRIMARY KEY,
    user_id          INTEGER   NOT NULL REFERENCES users(id)       ON DELETE CASCADE,
    species_id       INTEGER   NOT NULL REFERENCES bird_species(id) ON DELETE CASCADE,
    confidence_score FLOAT     NOT NULL,
    upload_path      VARCHAR(512) NOT NULL,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
