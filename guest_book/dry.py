def get_max_page(db, quantity,  name = None):

    '''Returns number of highest page to shown on main webpage'''
    if name:
        all_entries_nr = db.count_entries(name)
    else:
        all_entries_nr = db.count_entries()
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
