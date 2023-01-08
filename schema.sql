CREATE TABLE IF NOT EXISTS economy(
    userid BIGINT UNIQUE NOT NULL,
    balance INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS gearref(
    itemid SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    gearslot INTEGER NOT NULL,
    levelreq INTEGER DEFAULT 1,
    cost INTEGER DEFAULT 0,
    strength INTEGER DEFAULT 0,
    defence INTEGER default 0,
    crit FLOAT default 0.0,
    asset_name TEXT
);

CREATE TABLE IF NOT EXISTS gearinv(
    userid BIGINT NOT NULL,
    itemid BIGINT NOT NULL,
    modifier INTEGER DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS equippedgear(
    userid BIGINT NOT NULL,
    slot INTEGER NOT NULL,
    invref SERIAL NOT NULL
);

CREATE TABLE IF NOT EXISTS fishing(
    userid BIGINT UNIQUE NOT NULL,
    fishing_rod INTEGER DEFAULT 0,
    fish_caught INTEGER DEFAULT 0,
    experience INTEGER DEFAULT 0,
    bag_level INTEGER DEFAULT 0,
    quests_completed INTEGER DEFAULT 0,
    treasure_fished INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS caught_fish(
    userid BIGINT NOT NULL,
    fishid TEXT NOT NULL,
    amount INTEGER NOT NULL,
    CONSTRAINT userid_fishid UNIQUE (userid, fishid)
);

CREATE TABLE IF NOT EXISTS achievements_def(
    achievement_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    taskline TEXT NOT NULL,
    requirement INTEGER NOT NULL,
    custom_asset TEXT
);

CREATE TABLE IF NOT EXISTS achievements(
    userid BIGINT NOT NULL,
    achievement SERIAL NOT NULL,
    progress INTEGER DEFAULT 0,
    CONSTRAINT userid_achievement UNIQUE (userid, achievement)
);