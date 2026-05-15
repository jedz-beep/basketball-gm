-- Basketball GM — SQLite schema.
-- All attribute fields are 1-20 (see config.ATTRIBUTE_MIN/MAX).
-- Money is stored in whole euros (INTEGER).

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS leagues (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    country         TEXT    NOT NULL,
    team_count      INTEGER NOT NULL,
    regular_games   INTEGER NOT NULL,
    playoff_teams   INTEGER NOT NULL,
    foreign_limit   INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS teams (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id       INTEGER NOT NULL REFERENCES leagues(id),
    name            TEXT    NOT NULL UNIQUE,
    city            TEXT    NOT NULL,
    abbreviation    TEXT    NOT NULL,
    budget          INTEGER NOT NULL,
    prestige        INTEGER NOT NULL,
    fan_loyalty     INTEGER NOT NULL,
    arena_capacity  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS players (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id         INTEGER REFERENCES teams(id),
    first_name      TEXT    NOT NULL,
    last_name       TEXT    NOT NULL,
    nationality     TEXT    NOT NULL,
    is_domestic     INTEGER NOT NULL,          -- 1 = Israeli, 0 = foreign
    age             INTEGER NOT NULL,
    height_cm       INTEGER NOT NULL,
    position        TEXT    NOT NULL,          -- PG, SG, SF, PF, C

    -- Technical (11)
    three_point     INTEGER NOT NULL,
    mid_range       INTEGER NOT NULL,
    free_throws     INTEGER NOT NULL,
    finishing       INTEGER NOT NULL,
    post_moves      INTEGER NOT NULL,
    passing         INTEGER NOT NULL,
    ball_handling   INTEGER NOT NULL,
    steal           INTEGER NOT NULL,
    block           INTEGER NOT NULL,
    off_rebound     INTEGER NOT NULL,
    def_rebound     INTEGER NOT NULL,

    -- Physical (5)
    speed           INTEGER NOT NULL,
    strength        INTEGER NOT NULL,
    vertical        INTEGER NOT NULL,
    stamina         INTEGER NOT NULL,
    agility         INTEGER NOT NULL,

    -- Mental visible (5)
    basketball_iq   INTEGER NOT NULL,
    decision_making INTEGER NOT NULL,
    aggression      INTEGER NOT NULL,
    composure       INTEGER NOT NULL,
    leadership      INTEGER NOT NULL,

    -- Hidden (5)
    potential       INTEGER NOT NULL,
    work_ethic      INTEGER NOT NULL,
    professionalism INTEGER NOT NULL,
    consistency     INTEGER NOT NULL,
    injury_prone    INTEGER NOT NULL,

    -- Personality (3)
    ambition        INTEGER NOT NULL,
    loyalty         INTEGER NOT NULL,
    ego             INTEGER NOT NULL,

    morale          INTEGER NOT NULL DEFAULT 12
);

CREATE TABLE IF NOT EXISTS coaches (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id             INTEGER REFERENCES teams(id),
    first_name          TEXT    NOT NULL,
    last_name           TEXT    NOT NULL,
    role                TEXT    NOT NULL,     -- head, assistant, scout_head, fitness, academy
    age                 INTEGER NOT NULL,
    tactical_knowledge  INTEGER NOT NULL,
    player_development  INTEGER NOT NULL,
    man_management      INTEGER NOT NULL,
    rotation_philosophy INTEGER NOT NULL,
    gm_relationship     INTEGER NOT NULL,
    reputation          INTEGER NOT NULL,
    ambition            INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS contracts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id       INTEGER NOT NULL REFERENCES players(id),
    team_id         INTEGER NOT NULL REFERENCES teams(id),
    salary          INTEGER NOT NULL,
    length_years    INTEGER NOT NULL,
    years_remaining INTEGER NOT NULL,
    guarantee       TEXT    NOT NULL,         -- full, partial, none
    release_clause  INTEGER,
    player_option   INTEGER NOT NULL DEFAULT 0,
    team_option     INTEGER NOT NULL DEFAULT 0,
    no_trade        INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS seasons (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id       INTEGER NOT NULL REFERENCES leagues(id),
    year            INTEGER NOT NULL,
    current_day     INTEGER NOT NULL DEFAULT 1,
    phase           TEXT    NOT NULL DEFAULT 'preseason'
);

CREATE TABLE IF NOT EXISTS matches (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id       INTEGER NOT NULL REFERENCES seasons(id),
    home_team_id    INTEGER NOT NULL REFERENCES teams(id),
    away_team_id    INTEGER NOT NULL REFERENCES teams(id),
    scheduled_day   INTEGER NOT NULL,
    home_score      INTEGER,
    away_score      INTEGER,
    played          INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_players_team    ON players(team_id);
CREATE INDEX IF NOT EXISTS idx_contracts_team  ON contracts(team_id);
CREATE INDEX IF NOT EXISTS idx_contracts_player ON contracts(player_id);
CREATE INDEX IF NOT EXISTS idx_matches_season  ON matches(season_id);
