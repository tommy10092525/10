CREATE TABLE
    divisions (
        id PRIMARY KEY AUTOINCREMENT,
        name STRING,
        created_at DATETIME
    )
CREATE TABLE
    kinds (
        id PRIMARY KEY AUTOINCREMENT,
        name STRING,
        division_id INTEGER REFERENCES divisions,
        created_at DATETIME
    )
CREATE TABLE
    threads (
        id PRIMARY KEY AUTOINCREMENT,
        title STRING,
        kind_id INTEGER,
        created_at DATETIME
    )
CREATE TABLE
    responses (
        id PRIMARY KEY AUTOINCREMENT,
        content STRING,
        thread_id INTEGER,
        created_at DATETIME
    )