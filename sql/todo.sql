DROP TABLE IF EXISTS user_data;
DROP TABLE IF EXISTS todo;


CREATE TABLE user_data(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
	);


CREATE TABLE todo(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT,
	description TEXT NOT NULL,
	due_date DATE,
	status TEXT DEFAULT 'NOT DONE',
	FOREIGN KEY (username) references user_data(username) ON DELETE CASCADE
	);

