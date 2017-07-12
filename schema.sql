CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT,
    FOREIGN KEY (uid) REFERENCES users(id)
);

CREATE TABLE nodes_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT,
    FOREIGN KEY (uid) REFERENCES users(id)
);

CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY NOT NULL,
	username TEXT
);