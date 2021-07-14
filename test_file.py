import requests

from app.db_access import DB_access
from sqlite3 import OperationalError

db_location = '/home/misza/Projekty/Rekrutacja_2/app/test.db'



def test_pytest():

    '''Checks PyTest'''
    
    assert True
    assert not False



def test_clean_db():
    
    '''Cleans DB to prepare it to other tests '''
    
    with DB_access() as db:
        db = db.cursor
        try:
            db.execute('DELETE FROM user')
            db.execute('DELETE FROM post')
            db.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'user'")
            db.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'post'")
            db.commit()
            db.execute('VACUUM')
            assert True
        except OperationalError:
            assert False



def test_new_user():

    '''Adds fake user and then 
    checks if it is present in DB.
    One user is too short, second is ok, third is too long. 
    First assert checks, if adding user was ok (the return True)
    or not (return False). Second, whether user is already in DB
    (ther returns its ID) or not (returns None)
    
    '''

    users = ('', 'test_new_user',
            'oooooooooooooooooooooooooooooooooooooooo')
    
    with DB_access() as db:
        for user in users:
            result = db.add_user(user)
            assert result in (True, False)
            check = db.check_user(user)
            assert check == None or type(check) == int



def test_add_post():

    '''Adds post and user, if its not in DB.
    One post is too short, second is ok, third is too long.
    '''

    posts = ('',
    'Odpowiedni Post testowy',
    ('La La La La La ' * 200))
    
    user = 'test_add_post'

    with DB_access() as db:
        for post in posts:
            db.add_post(user = user, post_text = post)
            result = db.get_last_posts()
            for r in result:
                assert r[1] == 'Odpowiedni Post testowy'       
