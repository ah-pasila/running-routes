CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    type TEXT,
    length NUMERIC(5,1),
    created_at TIMESTAMP
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    route_id INTEGER REFERENCES routes
    grade INTEGER,
    review TEXT
);

