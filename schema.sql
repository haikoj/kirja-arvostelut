CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    review TEXT,
    grade INTEGER,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    comment TEXT NOT NULL,
    comment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
)

CREATE TABLE review_classes (
    id INTEGER PRIMARY KEY,
    review_id TEXT REFERENCES items,
    title TEXT,
    value TEXT
)