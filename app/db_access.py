import sqlite3 as sql
from datetime import datetime
from app.classes import Post



class DB_access:
    
    @staticmethod
    def __enter__(db_location = None):
        DB_access.cursor = sql.connect('/home/misza/Projekty/Rekrutacja_2/app/test.db')
        return DB_access
    
    @staticmethod
    def check_user(user):
        
        '''Checks, whether user is already in DB or not.
        If its true, it returns their id'''
        
        cmd = f'''
        SELECT DISTINCT id FROM user WHERE name = "{user}"; '''
        result = DB_access.cursor.execute(cmd)
        result = list(result)
        if result:
            return result[0][0]
    
    @staticmethod
    def add_user(user):
        
        '''Adds new user'''
        
        cmd = f'''
        INSERT INTO user (id, name) VALUES (:id, :name); '''
        insert = {'id': None,
                'name': user}
        result = DB_access.add_new(cmd, insert)
        return result
    
    @staticmethod
    def add_post(user, post_text):
        
        '''Adds posts and users
        first check whether autor is in DB, if not it creates them.
        Then it adds post text. It is only way to add user(user)'''
        
        user_key = DB_access.check_user(user)
        if not user_key:
            result = DB_access.add_user(user)
            if result:
                user_key = DB_access.cursor.execute('SELECT max(id) FROM user;')
                user_key = list(user_key)
                user_key = user_key[0][0]
        cmd = f'''
        INSERT INTO post (id, post_text, user, date) VALUES (:id, :post_text,:user, :date); '''
        insert = {'id': None,
                'post_text': post_text,
                'user': user_key,
                'date': str(datetime.now())}
        result = DB_access.add_new(cmd, insert)
        return result
    
    @staticmethod    
    def add_new(cmd, insert):
        
        '''Adds new data to base'''
        
        try:
            DB_access.cursor.execute(cmd, insert)
            DB_access.cursor.commit()
            return True
        except sql.IntegrityError:
            DB_access.cursor.rollback()
            # log entry error
            return False
    
    @staticmethod
    def get_posts(nr = None, quantity =  None, user = None):
        
        '''Select posts from database'''
        
        cmd = f'SELECT post.id, post.post_text, user.name, post.date FROM post LEFT JOIN user ON post.user = user.id '
        if nr:
            cmd += f'WHERE post.id = {nr} '
        if user:
            cmd += f'WHERE user.name = "{user}" '
        if quantity:
            cmd += f'ORDER BY date DESC LIMIT {quantity} '
        cmd += ';'
        print(cmd)
        source = DB_access.cursor.execute(cmd)
        for s in source:
            post = Post(s)
            yield post
    
    @staticmethod
    def __exit__(exc_type, exc_value, exc_traceback):
        DB_access.cursor.close()
        pass



new_base = False

if __name__ == '__main__' and new_base:
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
