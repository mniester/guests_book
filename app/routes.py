from flask import render_template, request
from app import app
from app.db_access import DB_access




@app.route('/', methods = ['POST', 'GET'])
def index():
    title = 'Księga Gości'
    with DB_access() as db:
        if request.method == 'GET':
            posts = db.get_last_posts(5)
            return render_template('index.html', title = title, posts = posts), 200
        else:
            data = request.get_json()
            result = db.add_post(user = data['user'], post_text = data['text'])
            posts = db.get_last_posts(5)
            if result:
                return render_template('index.html', title = title, posts = posts), 201
            else:
                return render_template('index.html', title = title, posts = posts), 400


