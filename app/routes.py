from flask import render_template, request, url_for, redirect, abort, flash
from app import app
from app.db_access import DB_access
from app.forms import Post_form

title = 'Księga Gości'



@app.route('/', methods = ['GET', 'POST'])
@app.route('/<quantity>', methods = ['GET'])
def index(quantity = 5, cut = 30):

    '''Returns group of latest posts (default - 5)'''

    with app.app_context():
        form = Post_form()
        with DB_access() as db:
            try:
                quantity = int(quantity)
            except ValueError:
                 quantity = 5
            if request.method == 'GET':
                posts = db.get_posts(quantity = quantity) 
                status_code = 200
                flash('')
            else:
                if form.validate_on_submit():
                    user = form.nick.data
                    post_text = form.text.data
                    result = db.add_post(user = user, post_text = post_text)
                    status_code = 201
                    flash('Twój wpis został dodany')
                else:
                    status_code = 400
                    flash('Twój wpis został odrzucony')
            posts = db.get_posts(quantity = quantity)
            return render_template('index.html', form = form, title = title, posts = posts, cut = cut), status_code



@app.route('/user/<name>/<quantity>')
@app.route('/user/<name>')
def user(name, quantity = 5, cut = 30):

    '''Returns group of latest posts (default - 5) of one user'''
    with app.app_context():
        form = Post_form()
        with DB_access() as db:
            try:
                quantity = int(quantity)
            except ValueError:
                 quantity = 5
            posts = list(db.get_posts(quantity = quantity, user = name))
            if posts:
                status_code = 200
                if len(posts) < int(quantity):
                    quantity = len(posts)
            else:
                abort(404)
            flash(f'Wyświetlono {quantity} wpisów użytkownika {name}')
            return render_template('index.html', form = form, title = title, posts = posts, cut = cut), status_code



@app.route('/post/<post_id>')
def full_post(post_id = None):

    '''Returns one, chosen post'''
    if post_id:
        with app.app_context():
            form = Post_form()
            with DB_access() as db:
                post = list(db.get_posts(nr = post_id))
                if post:
                    post = post[0]
                    status_code = 200
                    flash('')
                    return render_template('post.html', title = title, user = post.user, date = post.date, text = post.text), status_code
                else:
                    abort(404)
    else:
        abort(404)



@app.route('/api', methods = ['GET','POST'])
def api():

    '''Accepts posts as JSONs. It was added after adding form in 'index' route
    to preserve this capacity'''

    if request.method == 'GET':
        abort(404)
    else:
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
