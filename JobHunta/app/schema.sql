DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS watchlist;
DROP TABLE IF EXISTS popular;
DROP TABLE IF EXISTS applied;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS password_reset;
DROP TABLE IF EXISTS most_recent_searches;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL
);

CREATE TABLE applied (
  user_id INTEGER NOT NULL,
  job_id INTEGER NOT NULL,
  responded INTEGER NOT NULL,
  interviewed INTEGER NOT NULL,
  finalised INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (job_id) REFERENCES job(id)
);

CREATE TABLE watchlist (
  user_id INTEGER NOT NULL,
  job_id TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (job_id) REFERENCES job(id)
);

CREATE TABLE job (
  id TEXT PRIMARY KEY,
  title TEXT,
  job_type TEXT,
  description TEXT,
  location TEXT,
  company TEXT,
  created TEXT,
  url TEXT,
  salary INTEGER,
  in_watchlist BOOLEAN
);

CREATE TABLE popular (
  job_id TEXT NOT NULL,
  FOREIGN KEY (job_id) REFERENCES job(id)
);

CREATE TABLE password_reset (
    email TEXT UNIQUE,
    token TEXT,
    FOREIGN KEY (email) REFERENCES user(email)
);

CREATE TABLE searched_keywords (
  user_id INTEGER NOT NULL,
  keyword TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id)
);
--INSERT INTO user (username, password, first_name, last_name) VALUES ('qwer', 'qwer', 'qwer', 'qwer');
--SELECT * FROM user;
