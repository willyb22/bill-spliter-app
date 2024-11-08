CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    "timestamp" INTEGER,
    "description" INTEGER,
    FOREIGN KEY ("description") REFERENCES descriptions (id)
        ON UPDATE CASCADE
);