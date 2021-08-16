from json import load
from guest_book.db_access import DB_access

config_file = open('guest_book/config.json',)
config = load(config_file)

if __name__ == '__main__':
    with DB_access() as db:

        # I have saved table creation commands 
        # config is taken from JSON

        db.cursor.execute(f'''CREATE TABLE user
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE CHECK(length(name) > 1 AND length(name) <= {config["MAX_USER_LEN"]}));
        ''')
        db.cursor.execute(f'''CREATE TABLE entry
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        entry TEXT NOT NULL CHECK(length(entry) > 1 AND length(entry) <= {config["MAX_ENTRY_LEN"]}),
        user INTEGER NOT NULL,
        date TEXT NOT NULL CHECK (length(date) < 30),
        FOREIGN KEY(user) REFERENCES user(id));''')
