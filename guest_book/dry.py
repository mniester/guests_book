def add_entry(entry, db):
    
    '''Adds new entry'''
    
    user = entry.nick.data
    entry_text = entry.text.data
    result = db.add_entry(user = user, entry_text = entry_text)
    return result



def search_query(query, db, quantity):
    
    '''Query in Data Base'''
    
    data = query.query.data
    entries = db.get_entries(query = data, quantity = quantity)
    entries = list(entries)
    return entries



def post_method_handling(entry, query, db, quantity):
    
    '''Common funtion to handle post method'''
    
    if entry.write.data and entry.validate():
        result = add_entry(entry, db)
        if result:
            status_code = 201
            message = 'Twój wpis został dodany'
            entries = db.get_entries(quantity = quantity)
            return status_code, message, entries
    elif query.ask.data and query.validate():
        entries = search_query(query, db, quantity)
        if entries:
            status_code = 200
            message = 'Wyniki wyszukiwania'
        else:
            print('=============')
            status_code = 204
            message = 'Nic nie znaleziono'
            print(message)
        return status_code, message, entries
    entries = db.get_entries(quantity = quantity)
    return 400, 'Wpis nie spełnia wymagań', entries
    
