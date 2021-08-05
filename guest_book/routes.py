from flask import render_template, request, abort, make_response, jsonify


from guest_book import app
from guest_book.db_access import DB_access
from guest_book.dry import db_operations, query_message, display_data, get_max_page
from guest_book.forms import Entry


@app.route('/', methods = ['GET', 'POST'])
def index(quantity = None, page = 1, cut = app.config["CUT"]):

    f'''Returns group of latest entries (default - {app.config["ENTRIES"]})'''
    
    entry = Entry()
    quantity = request.args.get('quantity')
    page = request.args.get('page')
    print(quantity, page)
    quantity, offset = display_data(quantity, page, app)
    back = 'Odśwież'
    with DB_access() as db:
        max_page = get_max_page(db, quantity)
        if not max_page:
            abort(404)
        if request.method == 'GET':
            status_code = 200
            message = 'Może coś napiszesz?'
            entries = db.get_entries(quantity = quantity, offset = offset)
        else:
            status_code, message, entries = db_operations(db, entry, quantity)
            if status_code == 404:
                abort(404)
        if entries:
            template = 'entries.html'
        else:
            template = 'noentries.html'
        return render_template(template, back = back,
                                   entry = entry, 
                                   title = app.config['TITLE'],
                                   entries = entries,
                                   cut = cut,
                                   quantity = quantity,
                                   page = page,
                                   max_page = max_page,
                                   message = message), status_code


@app.route('/user/', methods = ['GET'])
def user(name = None, quantity = None, page = 1, cut = app.config["CUT"]):

    f'''Returns group of latest entries (default - {app.config["ENTRIES"]}) of one user'''

    entry = Entry()
    quantity = request.args.get('quantity')
    page = request.args.get('page')
    name = request.args.get('name')
    back = 'Pokaż wpisy wszystkich użytkowników'
    if name:
        app.config['NAME'] = name
    else:
        if name == '':
            abort(404)
        try:
            name = app.config['NAME']
        except KeyError:
            abort(404)
    with DB_access() as db:
        max_page = get_max_page(db, quantity, name)
        if not max_page:
            abort(404)
        quantity, offset = display_data(quantity, page, app)
        entries = list(db.get_entries(quantity = quantity, user = name, offset = offset))
        if entries:
            template = 'entries.html' 
        else:
            template = 'noentries.html'
        message = query_message(entries, name)
        status_code = 200
        return render_template(template, back = back,
                                   entry = entry, 
                                   title = app.config['TITLE'],
                                   entries = entries,
                                   cut = cut,
                                   quantity = quantity,
                                   page = page,
                                   max_page = max_page,
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
            result = db.get_entries(user = data['user'],
                                    quantity = data['quantity'])
            if result:
                output = {'user': [], 'date': [], 'text': []}
                for entry in result:
                    output['user'].append(entry.user)
                    output['date'].append(entry.date)
                    output['text'].append(entry.text)
                output = jsonify(output)
                return output
            else:
                status_code = '400'
        response = make_response('', status_code)
        return response


@app.errorhandler(404)
def page_not_found(e):
    back = 'Powrót do strony głównej'
    message = 'Nie ma takiej strony'
    return render_template('error_404.html', message = message, back = back), 404
