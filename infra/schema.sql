CREATE TABLE stats
    (
        id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
        uuid VARCHAR(128) NOT NULL,
        state VARCHAR(128) NOT NULL,
        hostname VARCHAR(128) NOT NULL,
        facility VARCHAR(128) NOT NULL,
        plan VARCHAR(128) NOT NULL,
        operating_system VARCHAR(128) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        creation_duration INTEGER NOT NULL
    );
