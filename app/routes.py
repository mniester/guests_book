from flask import render_template, request, url_for
from app import app
from app.db_access import DB_access
from app.forms import Post_form

title = 'Księga Gości'



@app.route('/', methods = ['GET', 'POST'])
@app.route('/<quantity>', methods = ['GET'])
def index(quantity = 5, cut = 30):

    '''Returns group of latest posts (default - 5)'''
    data = request.data
    print(data)
    with app.app_context():
        form = Post_form()
        with DB_access() as db:
            if request.method == 'GET':
                posts = db.get_posts(quantity = quantity) 
                status_code = 200
            else:
                if form.validate_on_submit():
                    user = form.nick.data
                    post_text = form.text.data
                    result = db.add_post(user = user, post_text = post_text)
                    status_code = 201
                else:
                    status_code = 400
            posts = db.get_posts(quantity = quantity)
            return render_template('index.html', form = form, title = title, posts = posts, cut = cut), status_code



@app.route('/user/<name>/<quantity>')
@app.route('/user/<name>')
def user(name, quantity = 5, cut = 30):

    '''Returns group of latest posts (default - 5) of one user'''

    with DB_access() as db:
        posts = list(db.get_posts(quantity = quantity, user = name))
        if posts:
            status_code = 200
        else:
            status_code = 204
        return render_template('index.html', title = title, posts = posts, cut = 30), status_code



@app.route('/post/<post_id>')
def full_post(post_id = None):

    '''Returns one, chosen post'''
    
    with DB_access() as db:
        post = list(db.get_posts(nr = post_id))[0]
        if post:
            status_code = 200
        else:
            status_code = 204
        return render_template('post.html', title = title,
        user = post.user, date = post.date, text = post.get_text(None)), status_code

