import sqlite3 as sql



class DB_access:
    
    temp = None
    
    @staticmethod
    def __enter__():
        DB_access.cursor = sql.connect('test.db')
        return DB_access
    
    @staticmethod
    def add_post(author, post_text):
        DB_access.temp = (author, post_text)
    
    @staticmethod
    def get_last_posts(nr = 1):
        return DB_access.temp
    
    @staticmethod
    def __exit__(exc_type, exc_value, exc_traceback):
        DB_access.cursor.close()
        pass

with DB_access() as db:
    #db.cursor.execute('''CREATE TABLE user
    #(id INT NOT NULL PRIMARY KEY,
    #name TEXT NOT NULL CHECK(length(name) < 16));
    #''')
    pass
    #db.cursor.execute('''CREATE TABLE post
    #(id INT NOT NULL PRIMARY KEY,
    #post_text TEXT NOT NULL CHECK(length(post_text) < 1000),
    #author INT NOT NULL,
    #    FOREIGN KEY(author) REFERENCES user(id));
    #''')
