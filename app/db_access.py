import sqlite3 as sql



class DB_access:
    
    @staticmethod
    def __enter__():
        DB_access.cursor = sql.connect('/home/misza/Projekty/Rekrutacja_2/app/test.db')
        return DB_access
    
    @staticmethod
    def check_user(user):
        
        '''This method check, whether user is already in DB or not.
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
        
        '''This method adds new user'''
        
        cmd = f'''
        INSERT INTO user (id, name) VALUES (:id, :name); '''
        insert = {'id': None,
                'name': user}
        result = DB_access.add_new(cmd, insert)
        return result
    
    @staticmethod
    def add_post(user, post_text):
        
        '''This method both add posts and users
        first check whether autor is in DB, if not it creates them.
        Then it adds post text. It is only way to add user(user)'''
        
        user_key = DB_access.check_user(user)
        if not user_key:
            user_key = DB_access.add_user(user)
        cmd = f'''
        INSERT INTO post (id, post_text, user) VALUES (:id, :post_text,:user); '''
        insert = {'id': None,
                'post_text': post_text,
                'user': user}
        DB_access.add_new(cmd, insert)
    
    @staticmethod
    def add_new(cmd, insert):
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
        if user:
            pass
        else:
            pass
        user = 'Autor Testowy'
        post_text = 'Treść Testowa'
        return (user, post_text)
    
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
            FOREIGN KEY(user) REFERENCES user(id));
        ''')
        user = 'user_0'
        db.add_user(user)
        pass
