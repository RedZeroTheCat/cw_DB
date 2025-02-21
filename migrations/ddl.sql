CREATE TYPE user_role AS ENUM ('user', 'master');
CREATE TYPE session_type AS ENUM ('online', 'offline', 'various');

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    social_media_link VARCHAR(255),
    age INT CHECK (age >= 0),
    role user_role NOT NULL,
    playing_since DATE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE Groups (
    group_id SERIAL PRIMARY KEY,
    master_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    group_name VARCHAR(255) NOT NULL,
    type session_type NOT NULL
);

CREATE TABLE GroupMembers (
    group_id INT NOT NULL REFERENCES Groups(group_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE Modules (
    module_id SERIAL PRIMARY KEY,
    module_name VARCHAR(255) NOT NULL,
    system_name VARCHAR(255) NOT NULL,
    description TEXT,
    group_size INT CHECK (group_size > 0)
);

CREATE TABLE Campaigns (
    campaign_id SERIAL PRIMARY KEY,
    group_id INT NOT NULL REFERENCES Groups(group_id) ON DELETE CASCADE,
    module_id INT NOT NULL REFERENCES Modules(module_id) ON DELETE CASCADE,
    duration INT CHECK (duration > 0),
    status VARCHAR(50) NOT NULL CHECK (status IN ('active', 'paused', 'completed')) DEFAULT ('active'),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Sessions (
    session_id SERIAL PRIMARY KEY,
    campaign_id INT NOT NULL REFERENCES Campaigns(campaign_id) ON DELETE CASCADE,
    session_date DATE NOT NULL,
    duration INT CHECK (duration > 0),
    notes TEXT
);

CREATE TABLE CharacterSheets (
    character_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    character_name VARCHAR(255) NOT NULL,
    attributes TEXT,
    background TEXT
);

CREATE TABLE Achievements (
    achievement_id SERIAL PRIMARY KEY,
    campaign_id INT NOT NULL REFERENCES Campaigns(campaign_id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES Users(user_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    date_awarded DATE NOT NULL
);

