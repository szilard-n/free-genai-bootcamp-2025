-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Create words table
CREATE TABLE IF NOT EXISTS words
(
    id      INTEGER PRIMARY KEY,
    german  TEXT NOT NULL,
    english TEXT NOT NULL,
    class   TEXT NOT NULL
);

-- Create groups table
CREATE TABLE IF NOT EXISTS groups
(
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    words_count INTEGER DEFAULT 0,
    description TEXT NOT NULL
);

-- Create word_groups join table
CREATE TABLE IF NOT EXISTS word_groups
(
    word_id  INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    PRIMARY KEY (word_id, group_id),
    FOREIGN KEY (word_id) REFERENCES words (id),
    FOREIGN KEY (group_id) REFERENCES groups (id)
);

-- Create study_activities table
CREATE TABLE IF NOT EXISTS study_activities
(
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url  TEXT NOT NULL
);

-- Create study_sessions table
CREATE TABLE IF NOT EXISTS study_sessions
(
    id                INTEGER PRIMARY KEY,
    group_id          INTEGER NOT NULL,
    study_activity_id INTEGER NOT NULL,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups (id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities (id)
);

-- Create word_review_items table
CREATE TABLE IF NOT EXISTS word_review_items
(
    id               INTEGER PRIMARY KEY,
    word_id          INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct          BOOLEAN NOT NULL,
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words (id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions (id)
);

-- Create trigger to maintain words_count in groups
CREATE TRIGGER IF NOT EXISTS update_group_words_count_insert
    AFTER INSERT
    ON word_groups
BEGIN
    UPDATE groups
    SET words_count = (SELECT COUNT(*)
                       FROM word_groups
                       WHERE group_id = NEW.group_id)
    WHERE id = NEW.group_id;
END;

CREATE TRIGGER IF NOT EXISTS update_group_words_count_delete
    AFTER DELETE
    ON word_groups
BEGIN
    UPDATE groups
    SET words_count = (SELECT COUNT(*)
                       FROM word_groups
                       WHERE group_id = OLD.group_id)
    WHERE id = OLD.group_id;
END;