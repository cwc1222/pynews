-- Create schema version table
CREATE TABLE IF NOT EXISTS schema_versions (
    version INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    applied_at DATETIME DEFAULT (datetime('now')),
    checksum TEXT NOT NULL
);

-- Initial schema
CREATE TABLE IF NOT EXISTS subscribers (
    email TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'pending',
    confirmation_token TEXT NOT NULL,
    created_at DATETIME DEFAULT (datetime('now')),
    updated_at DATETIME DEFAULT (datetime('now'))
);
