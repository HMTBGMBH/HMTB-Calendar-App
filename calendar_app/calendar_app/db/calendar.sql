CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    customer TEXT NOT NULL,
    location TEXT,
    event_type TEXT,
    comment TEXT,
    confirmation TEXT,
    document_type TEXT
);
