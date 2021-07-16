from flask import render_template, request, url_for, redirect, abort, flash
from app import app
from defaults import default_quantity, title
from app.db_access import DB_access
from app.dry import render_finish, post_method_handling
from app.forms import Post_form, Query_form



@app.route('/', methods = ['GET', 'POST'])
@app.route('/<quantity>', methods = ['GET', 'POST'])
def index(quantity = default_quantity, cut = 30):

    f'''Returns group of latest posts (default - {default_quantity})'''

    with app.app_context():
        post = Post_form()
        query = Query_form()
        back = 'Odśwież'
        with DB_access() as db:
            try:
                quantity = int(quantity)
            except ValueError:
                 quantity = default_quantity
            if request.method == 'GET':
                posts = db.get_posts(quantity = quantity) 
                status_code = 200
                message = 'Może coś napiszesz?'
            else:
                status_code, message, posts = post_method_handling(post, query, db, quantity)
            return render_finish(back, post, title, query, posts, cut, status_code, message, db, quantity)



@app.route('/user/<name>/<quantity>', methods = ['GET', 'POST'])
@app.route('/user/<name>', methods = ['GET', 'POST'])
def user(name, quantity = default_quantity, cut = 30):

    f'''Returns group of latest posts (default - {default_quantity}) of one user'''
    
    with app.app_context():
        post = Post_form()
        query = Query_form()
        back = 'Powrót do strony głównej'
        with DB_access() as db:
            if request.method == 'GET':
                try:
                    quantity = int(quantity)
                except ValueError:
                    quantity = default_quantity
                posts = list(db.get_posts(quantity = quantity, user = name))
                if posts:
                    status_code = 200
                    if len(posts) < int(quantity):
                        quantity = len(posts)
                    message = f'Wyświetlono {quantity} wpisów użytkownika {name}'
                else:
                    abort(404)
            else:
                status_code, message, posts = post_method_handling(post, query, db, quantity)
            return render_finish(back, post, title, query, posts, cut, status_code, message, db, quantity)



@app.route('/post/<post_id>')
def full_post(post_id = None):

    '''Returns one, chosen post'''
    if post_id:
        with app.app_context():
            post = Post_form()
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

    '''Accepts posts as JSONs. It was added after adding form in 'index' route
    to preserve this capacity'''

    data = request.json
    with DB_access() as db:
        result = db.add_post(user = data['user'], post_text = data['text'])
        if result:
            status_code = 201
        else:
            status_code = 400
        return redirect(url_for('index'), status_code)



@app.errorhandler(404)
def page_not_found(e):
    flash('Nie ma takiej strony')
    return redirect(url_for('index'), 404)
