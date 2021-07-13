import sqlite3 as sql
from datetime import datetime



class DB_access:
    
    @staticmethod
    def __enter__():
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
        else:
            None
    
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
            user_key = DB_access.add_user(user)
        cmd = f'''
        INSERT INTO post (id, post_text, user, date) VALUES (:id, :post_text,:user, :date); '''
        insert = {'id': None,
                'post_text': post_text,
                'user': user,
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
    def get_last_posts(nr = 1, user = None):
        cmd = f'SELECT * FROM post '
        if user:
            cmd = cmd[:-1] + f' WHERE name = {user}'
        cmd = cmd + f' ORDER BY date DESC LIMIT {nr};'
        source = DB_access.cursor.execute(cmd)
        for s in source:
            yield s
    
    @staticmethod
    def __exit__(exc_type, exc_value, exc_traceback):
        DB_access.cursor.close()
        pass



if __name__ == '__main__':
    with DB_access() as db:

        # I have saved and commented out table creation commands 

        db.cursor.execute('''CREATE TABLE user
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE CHECK(length(name) > 1 AND length(name) < 16));
        ''')
        db.cursor.execute('''CREATE TABLE post
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        post_text TEXT NOT NULL CHECK(length(post_text) > 1 AND length(post_text) < 1000),
        user INTEGER NOT NULL,
        date TEXT NOT NULL CHECK (length(date) < 30),
            FOREIGN KEY(user) REFERENCES user(id));
        ''')
        user = 'user_0'
        db.add_user(user)
        pass
