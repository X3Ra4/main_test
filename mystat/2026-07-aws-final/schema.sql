CREATE TABLE IF NOT EXISTS mood_entries (
    user_id bigint NOT NULL,
    day date NOT NULL,
    score smallint NOT NULL CHECK (score BETWEEN 1 AND 10),
    note varchar(500) NOT NULL DEFAULT '',
    PRIMARY KEY (user_id, day)
);
