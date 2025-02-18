CREATE TABLE IF NOT EXISTS word_reviews
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id       INTEGER NOT NULL,
    correct_count INTEGER   DEFAULT 0,
    wrong_count   INTEGER   DEFAULT 0,
    last_reviewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words (id)
);