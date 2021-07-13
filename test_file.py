import run
from app.db_access import DB_access



def test_pytest():

    '''Checks PyTest'''
    
    assert True
    assert not False



def test_new_user():

    '''Adds fake user and then 
    checks if it is present in DB
    
    One user is to short, second is ok, third to long
    
    '''

    users = ('', 'user_1',
            'oooooooooooooooooooooooooooooooooooooooo')
    
    with DB_access() as db:
        for user in users:
            result = db.add_user(user)
            assert result in (True, False)
            check = db.check_user(user)
            #breakpoint()
            assert check == None or type(check) == int



def test_add_post():

    '''Adds fake post and fake user, if its not in DB'''

    with DB_access() as db:
        user = 'user_1'
        post_text = 'TText to Check add'
        result = db.add_post(user, post_text)
