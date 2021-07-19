import requests
import json

from guest_book.db_access import DB_access
from sqlite3 import OperationalError
from flask import Response
from guest_book.forms import Entry, Query



app_adress = 'http://127.0.0.1:5000/'



def entries_generator(nr = 10, user = None, entry = None):
    if not user:
        user = 'test_user'
    if not entry:
        entry = str([a for a in range(100)])[1:-1]
    for x in range(nr):
        yield user, entry


generators_codes = ((entries_generator(10), 201),
                   (entries_generator(10, user ='x' * 25), 400), 
                   (entries_generator(10, entry = 'x' * 1100), 400))


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
            db.execute('DELETE FROM entry')
            db.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'user'")
            db.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'entry'")
            db.commit()
            db.execute('VACUUM')
            assert list(db.execute('SELECT * FROM user;')) == []
            assert list(db.execute('SELECT * FROM entry;')) == []
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



def test_add_entry():

    '''Adds entry and user, if its not in DB.
    One entry is too short, second is ok, third is too long.
    '''

    entries = ('',
    'Odpowiedni wpis testowy',
    ('La La La La La ' * 200))
    
    user = 'test_add_entry'

    with DB_access() as db:
        for entry in entries:
            db.add_entry(user = user, entry_text = entry)
            result = db.get_entries()
            for r in result:
                assert r.text == 'Odpowiedni wpis testowy'



def test_api():

    '''Tests API route'''

    api_adress = app_adress + 'api'
    with DB_access() as db:
        for generator, code in generators_codes:
            for entry in generator:
                try:
                    entry_in = {'user': entry[0], 
                               'text': entry[1], 
                               'mode': 'in'}
                    response = requests.post(api_adress, json = entry_in)
                    assert response.status_code == code
                    if code == 201:
                        entry_out = {'user': entry_in['user'], 
                                    'quantity': 1,
                                    'mode': 'out'}
                        response = requests.post(api_adress, json = entry_out)
                        assert response.status_code == 201
                except ConnectionError:
                    assert False

