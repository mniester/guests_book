from app.db_access import DB_access


if __name__ == '__main__':
    with DB_access() as db:

        # I have saved table creation commands 

        db.cursor.execute('''CREATE TABLE user
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE CHECK(length(name) > 1 AND length(name) < 16));
        ''')
        db.cursor.execute('''CREATE TABLE post
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        post_text TEXT NOT NULL CHECK(length(post_text) > 1 AND length(post_text) < 1000),
        user INTEGER NOT NULL,
        date TEXT NOT NULL CHECK (length(date) < 30),
        FOREIGN KEY(user) REFERENCES user(id));''')
