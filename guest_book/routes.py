from flask import render_template, request, url_for, redirect, abort, flash, make_response
from guest_book import app
from guest_book.defaults import default_quantity, title, default_cut
from guest_book.db_access import DB_access
from guest_book.dry import post_method_handling
from guest_book.forms import Entry_form, Query_form



@app.route('/', methods = ['GET', 'POST'])
@app.route('/<quantity>', methods = ['GET', 'POST'])
def index(quantity = default_quantity, cut = default_cut, entry = None, query = None):

    f'''Returns group of latest entries (default - {default_quantity})'''
    
    try:
        quantity = int(quantity)
    except ValueError:
        abort(404)
    
    if not entry and not query:
        entry = Entry_form()
        query = Query_form()
    back = 'Odśwież'
    with DB_access() as db:
        if request.method == 'GET':
            status_code = 200
            message = 'Może coś napiszesz?'
            posts = db.get_posts(quantity = quantity)
        else:
            status_code, message, posts = post_method_handling(entry, query, db, quantity)
        return render_template('index.html', back = back,
                                   entry = entry, 
                                   title = title,
                                   posts = posts,
                                   query = query,
                                   cut = cut), status_code




@app.route('/user/<name>/<quantity>', methods = ['GET', 'POST'])
@app.route('/user/<name>', methods = ['GET', 'POST'])
def user(name, quantity = default_quantity, cut = default_cut, entry = None, query = None):

    f'''Returns group of latest entries (default - {default_quantity}) of one user'''
    
    if not entry and not query:
        entry = Entry_form()
        query = Query_form()
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = default_quantity
    back = 'Odśwież'
    with DB_access() as db:
        if request.method == 'GET':
            posts = list(db.get_posts(user = name, quantity = quantity))
            if posts:
                message = f'Znaleziono {len(posts)} wpisów'
                status_code = 200
            else:
                abort(404)
        else:
            status_code, message, posts = post_method_handling(entry, query, db, quantity)
        return render_template('index.html', back = back,
                                   entry = entry, 
                                   title = title,
                                   posts = posts,
                                   query = query,
                                   cut = cut), status_code



@app.route('/post/<post_id>')
def full_post(post_id = None):

    '''Returns one, chosen post'''
    
    try:
        post_id = int(post_id)
    except ValueError:
        post_id = None
    
    if post_id:
        with DB_access() as db:
            post = list(db.get_posts(nr = post_id))
            if post:
                post = post[0]
                status_code = 200
                return render_template('post.html', 
                    title = title, 
                    user = post.user, 
                    date = post.date, 
                    text = post.text), status_code
            else:
                abort(404)
    else:
        abort(404)



@app.route('/api', methods = ['POST'])
def api():

    '''Accepts entries as JSONs. It was added after adding form in 'index' route
    to preserve this capacity'''

    data = request.json
    with DB_access() as db:
        result = db.add_post(user = data['user'], post_text = data['text'])
        if result:
            status_code = '201'
        else:
            status_code = '400'
        response = make_response('', status_code)
        return response



@app.errorhandler(404)
def page_not_found(e):
    back = 'Powrót do strony głównej'
    flash('Nie ma takiej strony')
    return render_template('error_404.html', back = back), 404
