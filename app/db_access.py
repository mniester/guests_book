import sqlite3 as sql



class DB_access:
    
    @staticmethod
    def __enter__():
        DB_access.cursor = sql.connect('test.db')
        return DB_access
    
    @staticmethod
    def check_author(author):
        cmd = f'''
        SELECT id FROM user WHERE name = {author}; '''
        result = DB_access.cursor.execute(cmd)
        return result
    
    @staticmethod
    def add_author(author):
        cmd = f'''
        INSERT INTO user (id, name) VALUES (:id, :name); '''
        insert = {'id': None,
                'name': author}
        #try:
        print(cmd)
        DB_access.cursor.execute(cmd, insert)
        DB_access.cursor.commit()
        #except sql.OperationalError:
        #    DB_access.cursor.rollback()
            # log entry error
    
    @staticmethod
    def add_post(author, post_text):
        if not DB_access.check_author:
            DB_access.add_author(author)
    
    @staticmethod
    def get_last_posts(nr = 1, author = None):
        if author:
            pass
        else:
            pass
    
    @staticmethod
    def __exit__(exc_type, exc_value, exc_traceback):
        DB_access.cursor.close()
        pass



with DB_access() as db:

    # I have saved and commented out table creation commands 

    db.cursor.execute('''CREATE TABLE user
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE CHECK(length(name) > 1 AND length(name) < 16));
    ''')
    db.cursor.execute('''CREATE TABLE post
    (id INT NOT NULL PRIMARY KEY,
    post_text TEXT NOT NULL CHECK(length(post_text) > 1 AND length(post_text) < 1000),
    author INT NOT NULL,
        FOREIGN KEY(author) REFERENCES user(id));
    ''')
    author = 'Autor Testowy'
    db.add_author(author)
