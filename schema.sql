CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    interest_profile TEXT
);

CREATE TABLE IF NOT EXISTS contents (
    id INTEGER PRIMARY KEY,
    title TEXT,
    category TEXT,
    tags TEXT,
    popularity INTEGER DEFAULT 0,
    date_added TEXT
);

CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content_id INTEGER,
    interaction_type TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(content_id) REFERENCES contents(id)
);
