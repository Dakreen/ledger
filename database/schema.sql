-- Database schema for events table
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    actor TEXT,
    action TEXT,
    details TEXT,
    prev_hash TEXT,
    hash TEXT
);

CREATE TABLE ledger_meta (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    total_events INTEGER,
    last_hash TEXT
);