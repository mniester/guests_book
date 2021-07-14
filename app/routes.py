from flask import render_template
from app import app
from app.db_access import DB_access

@app.route('/')
@app.route('/index')
def index():
    with DB_access() as db:
        posts = db.get_last_posts()
        return render_template('index.html', posts = posts)
