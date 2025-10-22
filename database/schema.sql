-- Database schema for events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    actor TEXT,
    action TEXT,
    details TEXT,
    prev_hash TEXT,
    hash TEXT
)