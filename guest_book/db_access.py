import sqlite3 as sql

from datetime import datetime
from guest_book.classes import Entry
from guest_book import app
from guest_book.dry import file_location


class DB_access:

    @staticmethod
    def __enter__():
        location = file_location(__file__)
        db_location = location + '/' + app.config['DB']
        DB_access.cursor = sql.connect(db_location)
        return DB_access

    @staticmethod
    def check_user(user, exact):

        '''Checks, whether user is already in DB or not.
        If its true, it returns their id.
        Has two modes - one is exact query, other regular expression search'''

        if exact:
            cmd = f'''
            SELECT id FROM user WHERE name = "{user}"; '''
        else:
            cmd = f''' SELECT id FROM user WHERE name LIKE "%{user}%"; '''
        result = DB_access.cursor.execute(cmd)
        result = list(result)
        if result:
            if exact:
                return result[0][0]
            else:
                result = tuple([x[0] for x in result])
                if len(result) == 1:
                    result = result[0]
                return result

    @staticmethod
    def add_user(user):
        
        '''Adds new user'''
        
        cmd = '''INSERT INTO user (id, name) VALUES (:id, :name); '''
        insert = {'id': None,
                'name': user}
        result = DB_access.add_new(cmd, insert)
        return result
    
    @staticmethod
    def add_entry(user, entry_text):

        '''Adds entries and users
        first check whether autor is in DB, if not it creates them.
        Then it adds entry text. It is only way to add user(user)'''

        user_key = DB_access.check_user(user, exact = True)
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
    def check_entries(user = None):

        '''Check how many entries are in the base'''

        cmd = 'SELECT COUNT(id) FROM entry ' 
        if user:
            users_ids = DB_access.check_user(user, exact = False)
            if users_ids:
                if type(users_ids) is tuple:
                    users_ids = str(users_ids)
                else:
                    users_ids = '(' + str(users_ids) + ')'
                cmd += f'WHERE user in {users_ids} '
        cmd += ';'
        nr = DB_access.cursor.execute(cmd)
        nr = list(nr)[0][0]
        return nr

    @staticmethod
    def get_entries(nr = None, user = None, query = None, 
        quantity = None, offset = None, exact = False):

        '''Select entries from database'''
        
        cmd = f'SELECT entry.id, entry.entry, user.name, entry.date FROM entry LEFT JOIN user ON entry.user = user.id '
        if nr:
            cmd += f'WHERE entry.id = {nr} ;'
            source = DB_access.cursor.execute(cmd)
            for s in source:
                entry = Entry(s)
                yield entry
        else:
            if user:
                cmd += 'WHERE '
                #if user:
                if exact:
                    cmd += f'user.name = "{user}" '
                else:
                    cmd += f'user.name LIKE "%{user}%" '
                if query:
                        cmd += "AND "
            if query:
                cmd += f'entry.entry LIKE "%{query}%" '
            cmd += 'ORDER BY date DESC '
            if quantity:
                cmd += f'LIMIT {quantity} '
            if offset and offset < DB_access.check_entries(user):
                cmd += f'OFFSET {offset} '
            cmd += ';'
            source = DB_access.cursor.execute(cmd)
            for s in source:
                entry = Entry(s)
                yield entry

    @staticmethod
    def __exit__(exc_type, exc_value, exc_traceback):
        DB_access.cursor.close()
