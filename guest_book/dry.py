def file_location(path):
    cut_point = path.rindex('/')
    location = path[:cut_point]
    return location



def query_response(entries):
    
    "Returns number of found entries with proper plural forms"
    
    found = len(entries)
    if str(found)[-1] == '1' and not (found >= 11 and found <= 19):
        end = ' wpis'
    elif str(found)[-1] in ('2','3','4'):
        end = ' wpisy'
    else:
        end = ' wpisów'
    response = f'Znaleziono {len(entries)}' + end
    return response



def add_entry(entry, db):
    
    '''Adds new entry'''
    
    user = entry.nick.data
    entry_text = entry.text.data
    result = db.add_entry(user = user, entry_text = entry_text)
    return result



def search_query(query, db, quantity):
    
    '''Query in Data Base'''
    
    data = query.entry.data
    entries = db.get_entries(query = data, quantity = quantity)
    entries = list(entries)
    return entries



def db_operations(db, entry, query, quantity, user = None):
    
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
        return status_code, message, entries
    elif query.ask.data and query.validate():
        entries = search_query(query, db, quantity)
        if entries:
            status_code = 200
            message = query_response(entries)
        else:
            status_code = 404
            message = None
    else:
        status_code = 400
        message = 'Wpis nie spełnia wymagań'
        entries = db.get_entries(quantity = quantity)
    return status_code, message, entries
    
