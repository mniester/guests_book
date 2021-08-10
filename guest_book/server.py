from flask import render_template, request, abort, make_response, jsonify


from guest_book import app
from guest_book.db_access import DB_access
from guest_book.dry import db_operations, query_message, get_offset, get_max_page


@app.route('/', methods = ['GET'])
def index():

    f'''Returns empty page'''

    template = 'index.html'
    return render_template(template,
                            max_entries = app.config['MAX_ENTRIES'],
                            entries_per_page = app.config["ENTRIES_PER_PAGE"],
                            max_entry_len = app.config["MAX_ENTRY_LEN"],
                            max_user_len = app.config["MAX_USER_LEN"],
                            title = app.config['TITLE'])


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


@app.route('/config', methods = ['GET'])
def config():
    
    '''Return default config to client'''
    
    data = request.args
    print(data['quantity'])
    try:
        quantity = request.args['quantity']
    except KeyError:
        quantity = app.config["ENTRIES_PER_PAGE"]
    with DB_access() as db:
        output = {'max_page': get_max_page(db, quantity, name = None),
                'quantity': app.config["ENTRIES_PER_PAGE"]}
        output = jsonify(output)
        return output


@app.route('/api', methods = ['GET', 'POST'])
def api():

    '''Accepts entries (using post HTTP method) 
    and return queries (using get HTTP method)'''

    if request.method == 'POST':
        data = request.get_json(force=True)
    else:
        data = request.args
    with DB_access() as db:
        if request.method == 'POST':
            result = db.add_entry(user = data['user'], entry_text = data['text'])
            if result:
                status_code = '201'
            else:
                status_code = '400'
        else:
            if not data['quantity']:
                data = dict(data)
                data['quantity'] = app.config["ENTRIES_PER_PAGE"]
            offset = get_offset(data['quantity'], data['page'], app)
            result = db.get_entries(user = data['user'],
                                    quantity = data['quantity'],
                                    offset = offset)
            if result:
                output = {'user': [], 'date': [], 'text': []}
                for entry in result:
                    output['user'].append(entry.user)
                    output['date'].append(entry.date)
                    output['text'].append(entry.get_text(app.config['CUT']))
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
