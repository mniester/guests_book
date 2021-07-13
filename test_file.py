import run
from app.db_access import DB_access



def test_pytest():

    '''Checks PyTest'''
    
    assert True
    assert not False



def test_new_user():

    '''Adds fake user and then 
    checks if it is present in DB.
    One user is too short, second is ok, third is too long. 
    First assert checks, if adding user was ok (the return True)
    or not (return False). Second, whether user is already in DB
    (ther returns its ID) or not (returns None)
    
    '''

    users = ('', 'user_1',
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
    ('La La La La La ' * 1000))
    
    user = 'test_add_post'

    with DB_access() as db:
        for post in posts:
            db.add_post(user = user, post_text = post)     