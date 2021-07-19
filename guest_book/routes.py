from flask import render_template, request, url_for, redirect, abort, make_response, jsonify
from guest_book import app
from guest_book.db_access import DB_access
from guest_book.dry import post_method_handling, query_response
from guest_book.forms import Entry, Query, Set_nr, Find_user
from guest_book import app



@app.route('/', methods = ['GET', 'POST'])
@app.route('/<quantity>', methods = ['GET', 'POST'])
def index(quantity = app.config["ENTRIES"], cut = app.config["CUT"]):

    f'''Returns group of latest entries (default - {app.config["ENTRIES"]})'''
    
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = app.config['ENTRIES']
    entry = Entry()
    query = Query()
    set_quantity = Set_nr()
    find_user = Find_user()
    back = 'Odśwież'
    with DB_access() as db:
        if request.method == 'GET':
            if find_user.data and find_user.validate():
                redirect(url_for('user', name = find_user.data.who))
            status_code = 200
            message = 'Może coś napiszesz?'
            entries = db.get_entries(quantity = quantity)
        else:
            status_code, message, entries = post_method_handling(entry, query, set_quantity, db, quantity)
            if status_code == 404:
                abort(404)
        return render_template('index.html', back = back,
                                   entry = entry, 
                                   title = app.config['TITLE'],
                                   entries = entries,
                                   query = query,
                                   cut = cut,
                                   set_quantity = set_quantity,
                                   find_user = find_user,
                                   message = message), status_code



@app.route('/user?name=<name>', methods = ['GET', 'POST'])
@app.route('/user/<name>/<quantity>', methods = ['GET', 'POST'])
@app.route('/user/<name>', methods = ['GET', 'POST'])
def user(name, quantity = app.config["ENTRIES"], cut = app.config["CUT"]):

    f'''Returns group of latest entries (default - {app.config["ENTRIES"]}) of one user'''
    
    name = request.form['name']
    print(data)
    entry = Entry()
    query = Query()
    set_quantity = Set_nr()
    find_user = Find_user()
    back = 'Pokaż wszystkie wpisy'
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = default_quantity
    with DB_access() as db:
        if request.method == 'GET':
            entries = list(db.get_entries(user = name, quantity = quantity))
            if entries:
                print('==============', name)
                message = query_response(entries)
                status_code = 200
            else:
                print('--------------')
                abort(404)
        else:
            status_code, message, entries = post_method_handling(entry, query, set_quantity, db, quantity, name)
            if not entries:
                abort(404)
        return render_template('index.html', back = back,
                                   entry = entry, 
                                   title = app.config['TITLE'],
                                   entries = entries,
                                   query = query,
                                   cut = cut,
                                   set_quantity = set_quantity,
                                   find_user = find_user,
                                   message = message), status_code



@app.route('/entry/<entry_id>')
def full_entry(entry_id):

    '''Returns one, chosen entry'''
    
    try:
        entry_id = int(entry_id)
    except ValueError:
        abort(404)
    
    with DB_access() as db:
        entry = list(db.get_entries(nr = entry_id))
        if entry:
            entry = entry[0]
            status_code = 200
            return render_template('entry.html', 
                title = app.config["TITLE"], 
                user = entry.user, 
                date = entry.date, 
                text = entry.text), status_code
        else:
            abort(404)



@app.route('/api', methods = ['POST'])
def api():

    '''Accepts entries as JSONs. It was added after adding form in 'index' route
    to preserve this capacity'''

    data = request.json
    with DB_access() as db:
        output = ''
        if data['mode'] == 'in':
            result = db.add_entry(user = data['user'], entry_text = data['text'])
            if result:
                status_code = '201'
            else:
                status_code = '400'
        else:
            result = db.get_entries(data['quantity'])
            if result:
                output = {'user': [], 'date': [], 'text': []}
                for entry in result:
                    output['user'].append(entry.user)
                    output['date'].append(entry.date)
                    output['text'].append(entry.text)
                output = jsonify(output)
                status_code = '201'
            else:
                status_code = '400'
        response = make_response(output, status_code)
        return response



@app.errorhandler(404)
def page_not_found(e):
    back = 'Powrót do strony głównej'
    message = 'Nie ma takiej strony'
    return render_template('error_404.html', message = message, back = back), 404
