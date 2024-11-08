CREATE TABLE IF NOT EXISTS transaction_detail (
    id INTEGER PRIMARY KEY,
    transaction_id INTEGER,
    participant_id INTEGER,
    proportion REAL DEFAULT 1,
    amount REAL DEFAULT 0,
    FOREIGN KEY (transaction_id) REFERENCES transactions (id)
        ON DELETE CASCADE,
    FOREIGN KEY (participant_id) REFERENCES participant (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);