CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role INTEGER
);

CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    length NUMERIC(5,1),
    created_at TIMESTAMP,
    created_by INTEGER REFERENCES users
);

CREATE TABLE maps (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    route_id INTEGER REFERENCES routes,
    data BYTEA
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    route_id INTEGER REFERENCES routes,
    grade INTEGER NOT NULL,
    review TEXT NOT NULL
);
