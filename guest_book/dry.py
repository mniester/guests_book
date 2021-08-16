def get_max_page(db, quantity, name = None, text_piece = None):

    '''Returns number of highest page to shown on main webpage'''

    all_entries_nr = db.count_entries(name, text_piece)
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