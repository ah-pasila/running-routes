CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    length NUMERIC(5,1),
    created_at TIMESTAMP,
    created_by INTEGER REFERENCES users
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    route_id INTEGER REFERENCES routes,
    grade INTEGER NOT NULL,
    review TEXT NOT NULL
);
