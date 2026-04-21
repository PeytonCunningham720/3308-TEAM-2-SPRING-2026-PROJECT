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
    ref_audio_path  VARCHAR(512),
    ref_spec_path   VARCHAR(512),
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

-- 4) Bird Species Data
INSERT INTO bird_species (common_name, scientific_name, description, ref_image) VALUES
('american_robin', 'Turdus migratorius', 'The American Robin is a migratory songbird with a distinctive orange-red breast and dark back. It is one of the most familiar birds across North America, often seen pulling earthworms from lawns. Robins are known for their cheerful, melodic song which signals the arrival of spring.', 'bird_images/american_robin.jpg'),
('common_loon', 'Gavia immer', 'The Common Loon is a large diving bird known for its haunting, wailing calls that echo across northern lakes. It has striking black and white plumage in summer and is an expert underwater swimmer, diving up to 200 feet to catch fish.', 'bird_images/common_loon.jpg'),
('mourning_dove', 'Zenaida macroura', 'The Mourning Dove is a slender, graceful bird with a soft cooing call that many find mournful and soothing. It is one of the most abundant birds in North America and a common sight at backyard feeders, foraging for seeds on the ground.', 'bird_images/mourning_dove.jpg'),
('pine_warbler', 'Setophaga pinus', 'The Pine Warbler is a small songbird that spends most of its life in pine forests. Males are bright yellow with white wing bars. Its trilling song is a signature sound of southeastern pine woodlands throughout the year.', 'bird_images/pine_warbler.jpg'),
('sandhill_crane', 'Antigone canadensis', 'The Sandhill Crane is a large, long-legged wading bird with a distinctive red forehead and bugling call. One of the oldest living bird species, sandhill cranes are famous for their spectacular migration flocks and elaborate courtship dances.', 'bird_images/sandhill_crane.jpg');
