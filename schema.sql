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