import sqlite3 as sql
from datetime import datetime
from guest_book.classes import Entry



class DB_access:
    
    @staticmethod
    def __enter__():
        DB_access.cursor = sql.connect('/home/misza/Projekty/Rekrutacja_2/guest_book/test.db')
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
    def add_entry(user, entry_text):
        
        '''Adds entries and users
        first check whether autor is in DB, if not it creates them.
        Then it adds entry text. It is only way to add user(user)'''
        
        user_key = DB_access.check_user(user)
        if not user_key:
            result = DB_access.add_user(user)
            if result:
                user_key = DB_access.cursor.execute('SELECT max(id) FROM user;')
                user_key = list(user_key)
                user_key = user_key[0][0]
        cmd = f'''
        INSERT INTO entry (id, entry, user, date) VALUES (:id, :entry,:user, :date); '''
        insert = {'id': None,
                'entry': entry_text,
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
    def get_entries(nr = None, user = None, query = None, quantity = None):
        
        '''Select entries from database'''
        
        cmd = f'SELECT entry.id, entry.entry, user.name, entry.date FROM entry LEFT JOIN user ON entry.user = user.id '
        if nr:
            cmd += f'WHERE entry.id = {nr} '
        elif user:
            cmd += f'WHERE user.name = "{user}" '
        elif query:
            cmd += f'WHERE entry.entry LIKE "%{query}%" '
        cmd += 'ORDER BY date DESC '
        if quantity:
             cmd += f'LIMIT {quantity} '
        cmd += ';'
        source = DB_access.cursor.execute(cmd)
        print(cmd)
        for s in source:
            entry = Entry(s)
            yield entry
    
    @staticmethod
    def __exit__(exc_type, exc_value, exc_traceback):
        DB_access.cursor.close()
