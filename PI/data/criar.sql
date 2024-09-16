-- SQLite
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    meeting_date DATE NOT NULL,
    document_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase TEXT NOT NULL,
    activity TEXT NOT NULL,
    responsible TEXT NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    area TEXT NOT NULL,
    observations TEXT,
    project_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);