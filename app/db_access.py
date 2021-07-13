import sqlite3 as sql



class DB_access:
    
    @staticmethod
    def __enter__():
        DB_access.cursor = sql.connect('test.db')
        return DB_access
    
    @staticmethod
    def __exit__(exc_type, exc_value, exc_traceback):
        DB_access.cursor.close()
        pass

with DB_access() as db:
    pass
