DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS watchlist;
DROP TABLE IF EXISTS popular;


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
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (job_id) REFERENCES job(id)
);

CREATE TABLE watchlist (
  user_id INTEGER NOT NULL,
  job_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (job_id) REFERENCES job(id)
);

CREATE TABLE job (
  id INTEGER PRIMARY KEY,
  title TEXT,
  job_type TEXT,
  description TEXT,
  location TEXT,
  company TEXT,
  url TEXT,
  salary INTEGER
);

CREATE TABLE popular (
  job_id INTEGER NOT NULL,
  FOREIGN KEY (job_id) REFERENCES job(id)
);

--INSERT INTO user (username, password, first_name, last_name) VALUES ('qwer', 'qwer', 'qwer', 'qwer');
--SELECT * FROM user;
