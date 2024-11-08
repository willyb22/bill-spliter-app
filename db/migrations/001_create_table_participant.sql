CREATE TABLE IF NOT EXISTS participant (
    id INTEGER PRIMARY KEY,
    "name" TEXT UNIQUE NOT NULL,
    is_active INTEGER DEFAULT 1 CHECK (is_active in (0, 1))
);