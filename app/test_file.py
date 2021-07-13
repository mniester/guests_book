import sqlite3 as sql
from .db_access import DB_access



def test_pytest():
    assert True
    assert not False

def test_new_post():
    with DB_access() as db:
        author = 'Autor Testowy'
        post_text = 'Treść Testowa'
        db.add_post(author = author, post_text = post_text)
        last_author, last_post_text = db.get_last_posts(nr = 1)
        assert author == last_author and post_text == last_post_text
