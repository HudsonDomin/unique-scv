PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY,
    number INTEGER,
    location TEXT,
    plate TEXT,
    model TEXT,
    is_attended INTEGER CHECK (is_attended IN (0, 1)),
    attended_by TEXT,
    attended_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_priority INTEGER CHECK (is_priority IN (0, 1))
);

CREATE INDEX IF NOT EXISTS idx_calls_created_at ON calls(created_at);
CREATE INDEX IF NOT EXISTS idx_calls_is_attended ON calls(is_attended);
CREATE INDEX IF NOT EXISTS idx_calls_attended_by ON calls(attended_by);
CREATE INDEX IF NOT EXISTS idx_calls_is_priority ON calls(is_priority);