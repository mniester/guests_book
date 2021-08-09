def get_max_page(db, quantity, name = None):

    '''Returns number of highest page to shown on main webpage'''

    if name:
        all_entries_nr = db.check_entries(name)
    else:
        all_entries_nr = db.check_entries()
    if all_entries_nr:
        quantity = int(quantity)
        full_pages = all_entries_nr // quantity
        if (full_pages * quantity) < all_entries_nr:
            return full_pages + 1
        return full_pages


def get_offset(quantity, page, app):

    """Counts value of offset for DB operations"""

    if not page:
        page = app.config['PAGE']
    offset = int(quantity) * (int(page) - 1)
    return offset


def file_location(path):

    '''Return location of file
    Takes its full path as argument'''

    cut_point = path.rindex('/')
    location = path[:cut_point]
    return location


def query_message(entries, user = None):

    "Returns number of found entries with proper plural forms in Polish"

    found = len(entries)
    if str(found)[-1] == '1' and not (found >= 11 and found <= 19):
        end = ' wpis'
    elif str(found)[-1] in ('2','3','4'):
        end = ' wpisy'
    else:
        end = ' wpisów'
    response = f'Wyświetlono {len(entries)}' + end
    if user:
        response += f', zapytanie o użytkownika: {user}'
    return response


def add_entry(entry, db):

    '''Adds new entry'''

    user = entry.user.data
    entry_text = entry.text.data
    result = db.add_entry(user = user, entry_text = entry_text)
    return result


def entry_query(entry, db, quantity):

    '''Query for entry in data base'''

    data = entry.text.data
    entries = db.get_entries(query = data, quantity = quantity)
    entries = list(entries)
    return entries


def user_query(db, quantity, user):

    '''Query for user in data base'''

    entries = db.get_entries(quantity = quantity, user = user)
    entries = list(entries)
    return entries


def db_operations(db, entry, quantity, user = None):

    '''Common funtion to handle db operations method'''

    if entry.write.data and entry.validate():
        result = add_entry(entry, db)
        if result:
            status_code = 201
            message = 'Twój wpis został dodany'
        else:
            status_code = 201
            message = 'Wpis jest nieprawidłowy'
        entries = db.get_entries(quantity = quantity)
    elif entry.query.data and entry.text.validate(entry):
        entries = entry_query(entry, db, quantity)
        if entries:
            status_code = 200
            message = query_message(entries)
        else:
            status_code = 404
            message = None
    elif user:
        entries = user_query(db, quantity, user)
        if entries:
            status_code = 200
            message = query_message(entries)
        else:
            status_code = 404
            message = None
    else:
        status_code = 400
        message = 'Polecenie nie spełnia wymagań'
        entries = db.get_entries(quantity = quantity)
    return status_code, message, entries
