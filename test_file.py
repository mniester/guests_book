import requests

from app.db_access import DB_access
from sqlite3 import OperationalError
from flask import Response



app_adress = 'http://127.0.0.1:5000/'



def posts_generator(nr = 10):
    text = str([a for a in range(100)])[1:-1]
    for x in range(nr):
        yield 'gen_user', text



def inproper_post_generator_1(nr = 10):
    for x in range(10):
        yield '', 'text_ok'



def inproper_post_generator_2(nr = 10):
    for x in range(10):
        yield 'user_ok', 'lalala' * 700



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
            assert list(db.execute('SELECT * FROM user;')) == []
            assert list(db.execute('SELECT * FROM post;')) == []
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
                assert r.text == 'Odpowiedni Post testowy'



def test_add_flask():
    generators_codes = ((posts_generator, 201),
                       (inproper_post_generator_1, 400), 
                       (inproper_post_generator_2, 400))
    with DB_access() as db:
        for generator, code in generators_codes:
            for p in generator(10):
                try:
                    post = {'user': p[0], 'text': p[1]}
                    r = requests.post(app_adress, json = post)
                    assert r.status_code == code
                except ConnectionError:
                    assert False
