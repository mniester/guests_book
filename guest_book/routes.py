from flask import render_template, request, url_for, redirect, abort, make_response, jsonify


from guest_book import app
from guest_book.db_access import DB_access
from guest_book.dry import db_operations, query_message
from guest_book.forms import Entry
from guest_book import app



@app.route('/', methods = ['GET', 'POST'])
def index(quantity = None, cut = app.config["CUT"]):

    f'''Returns group of latest entries (default - {app.config["ENTRIES"]})'''
    
    entry = Entry()
    quantity = request.args.get('quantity')
    if quantity:
        app.config["ENTRIES"] = quantity
    else:
        quantity = app.config["ENTRIES"]
    back = 'Odśwież'
    with DB_access() as db:
        if request.method == 'GET':
            status_code = 200
            message = 'Może coś napiszesz?'
            entries = db.get_entries(quantity = quantity)
        else:
            status_code, message, entries = db_operations(db, entry, quantity)
            if status_code == 404:
                abort(404)
        if entries:
            page = 'entries.html'
        else:
            page = 'noentries.html'
        return render_template(page, back = back,
                                   entry = entry, 
                                   title = app.config['TITLE'],
                                   entries = entries,
                                   cut = cut,
                                   quantity = quantity,
                                   message = message), status_code



@app.route('/user/', methods = ['GET'])
def user(name = None, quantity = None, cut = app.config["CUT"]):

    f'''Returns group of latest entries (default - {app.config["ENTRIES"]}) of one user'''

    entry = Entry()
    quantity = request.args.get('quantity')
    if quantity:
        app.config["ENTRIES"] = quantity
    else:
        quantity = app.config["ENTRIES"]
    status_code = 200
    back = 'Pokaż wpisy wszystkich użytkowników'
    name = request.args.get('name')
    if name:
        app.config['NAME'] = name
    else:
        try:
            name = app.config['NAME']
        except KeyError:
            abort(404)
    with DB_access() as db:
        entries = list(db.get_entries(quantity = quantity, user = name))
        if entries:
            page = 'entries.html' 
        else:
            page = 'noentries.html'
        message = query_message(entries, name)
        return render_template(page, back = back,
                                   entry = entry, 
                                   title = app.config['TITLE'],
                                   entries = entries,
                                   cut = cut,
                                   quantity = quantity,
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
                quantity = app.config["ENTRIES"],
                text = entry.text), status_code
        else:
            abort(404)



@app.route('/api', methods = ['POST'])
def api():

    '''Accepts entries as JSONs.'''

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
