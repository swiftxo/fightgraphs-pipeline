-- Cleaned schema for PostgreSQL

CREATE TABLE bonus (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE promotion (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(100) NOT NULL,
    ufcstats_url VARCHAR(255) NOT NULL,
    promotion_id INTEGER NOT NULL REFERENCES promotion(id)
);

CREATE TABLE fighter (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    nickname VARCHAR(100),
    date_of_birth DATE,
    height_cm NUMERIC(5,2),
    weight_kg NUMERIC(5,2),
    reach_cm NUMERIC(5,2),
    stance VARCHAR(50) NOT NULL,
    image_url VARCHAR(255),
    ufcstats_url VARCHAR(255) NOT NULL
);

CREATE TABLE referee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE judge (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE weightclass (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    min_weight_kg NUMERIC(5,2),
    max_weight_kg NUMERIC(5,2),
    gender VARCHAR(10) NOT NULL,
    promotion_id INTEGER NOT NULL REFERENCES promotion(id)
);

CREATE TABLE timeformat (
    id SERIAL PRIMARY KEY,
    format_string TEXT NOT NULL UNIQUE,
    base_rounds INTEGER,
    base_round_duration INTEGER NOT NULL,
    overtime_rounds INTEGER DEFAULT 0,
    overtime_duration INTEGER,
    unlimited_rounds BOOLEAN DEFAULT FALSE,
    no_time_limit BOOLEAN DEFAULT FALSE
);

CREATE TABLE fight (
    id SERIAL PRIMARY KEY,
    method VARCHAR(50),
    finish_details VARCHAR(255),
    time_format_id INTEGER NOT NULL REFERENCES timeformat(id),
    round_finished INTEGER,
    time_finished TIME,
    event_id INTEGER NOT NULL REFERENCES event(id),
    fighter1_id INTEGER NOT NULL REFERENCES fighter(id),
    fighter2_id INTEGER NOT NULL REFERENCES fighter(id),
    winner_id INTEGER REFERENCES fighter(id),
    weight_class_id INTEGER NOT NULL REFERENCES weightclass(id),
    referee_id INTEGER REFERENCES referee(id),
    ufcstats_url VARCHAR(255) NOT NULL,
    card_posigtion INTEGER
);

CREATE TABLE fighterrecord (
    id SERIAL PRIMARY KEY,
    fighter_id INTEGER NOT NULL REFERENCES fighter(id),
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    no_contests INTEGER DEFAULT 0
);

CREATE TABLE fightstat (
    id SERIAL PRIMARY KEY,
    round INTEGER NOT NULL,
    significant_strikes_attempted INTEGER DEFAULT 0,
    significant_strikes_landed INTEGER DEFAULT 0,
    total_strikes_landed INTEGER DEFAULT 0,
    total_strikes_attempted INTEGER DEFAULT 0,
    knockdowns INTEGER DEFAULT 0,
    takedowns_landed INTEGER DEFAULT 0,
    takedowns_attempted INTEGER DEFAULT 0,
    submissions_attempted INTEGER DEFAULT 0,
    reversals INTEGER DEFAULT 0,
    control_time_seconds INTEGER DEFAULT 0,
    head_strikes_landed INTEGER DEFAULT 0,
    head_strikes_attempted INTEGER DEFAULT 0,
    body_strikes_landed INTEGER DEFAULT 0,
    body_strikes_attempted INTEGER DEFAULT 0,
    leg_strikes_landed INTEGER DEFAULT 0,
    leg_strikes_attempted INTEGER DEFAULT 0,
    ground_strikes_landed INTEGER DEFAULT 0,
    ground_strikes_attempted INTEGER DEFAULT 0,
    clinch_strikes_landed INTEGER DEFAULT 0,
    clinch_strikes_attempted INTEGER DEFAULT 0,
    distance_strikes_landed INTEGER DEFAULT 0,
    distance_strikes_attempted INTEGER DEFAULT 0,
    fighter_id INTEGER NOT NULL REFERENCES fighter(id),
    fight_id INTEGER NOT NULL REFERENCES fight(id)
);

CREATE TABLE fightbonus (
    id SERIAL PRIMARY KEY,
    amount NUMERIC(10,2) NOT NULL,
    fight_id INTEGER NOT NULL REFERENCES fight(id),
    fighter_id INTEGER NOT NULL REFERENCES fighter(id),
    bonus_id INTEGER NOT NULL REFERENCES bonus(id)
);

CREATE TABLE scorecard (
    id SERIAL PRIMARY KEY,
    fight_id INTEGER NOT NULL REFERENCES fight(id),
    judge_id INTEGER NOT NULL REFERENCES judge(id),
    fighter_id INTEGER NOT NULL REFERENCES fighter(id),
    scorecard INTEGER NOT NULL
);

CREATE TABLE title (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    title_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL,
    weightclass_id INTEGER REFERENCES weightclass(id)
);

CREATE TABLE titlefight (
    id SERIAL PRIMARY KEY,
    fight_id INTEGER NOT NULL REFERENCES fight(id),
    title_id INTEGER NOT NULL REFERENCES title(id)
);