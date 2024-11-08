CREATE TABLE IF NOT EXISTS states (
    id INTEGER PRIMARY KEY,
    participant_id INTEGER,
    participant_to INTEGER,
    amount REAL DEFAULT 0,
    last_update INTEGER,
    CHECK (participant_id<participant_to),
    FOREIGN KEY (participant_id) REFERENCES participant (id) 
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (participant_to) REFERENCES participant (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);