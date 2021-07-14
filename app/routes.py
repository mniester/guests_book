from flask import render_template, request
from app import app
from app.db_access import DB_access



@app.route('/', methods = ['POST', 'GET'])
@app.route('/<nr>', methods = ['POST', 'GET'])
def index(nr = 5):
    nr_of_posts = nr
    title = 'Księga Gości'
    with DB_access() as db:
        if request.method == 'GET':
            posts = db.get_last_posts(nr_of_posts) 
            status_code = 200
        else:
            data = request.get_json()
            result = db.add_post(user = data['user'], post_text = data['text'])
            posts = db.get_last_posts(nr_of_posts)
            if result:
                status_code = 201
            else:
                status_code = 400
        return render_template('index.html', title = title, posts = posts), status_code



@app.route('/<name>/<nr>')
def author(name, nr = 5):
    nr_of_posts = nr
    with DB_access() as db:
        posts = db.get_last_posts(nr = nr_of_posts, user = name)
