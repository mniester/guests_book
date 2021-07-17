def add_post(post, db):
    
    '''Adds new post'''
    
    user = post.nick.data
    post_text = post.text.data
    result = db.add_post(user = user, post_text = post_text)
    return result



def search_query(query, db):
    
    '''Query in Data Base'''
    
    data = query.query.data
    posts = db.get_posts(query = data)
    posts = list(posts)
    return posts



def post_method_handling(entry, query, db, quantity):
    
    '''Common funtion to handle post method'''
    
    if entry.write.data and entry.validate():
        result = add_post(entry, db)
        if result:
            status_code = 201
            message = 'Twój wpis został dodany'
    elif query.ask.data and query.validate():
        posts = search_query(query, db)
        if posts:
            status_code = 201
            message = 'Wyniki wyszukiwania'
        else:
            status_code = 204
            message = 'Nic nie znaleziono'
        return status_code, message, posts
    posts = db.get_posts(quantity = quantity)
    return 205, 'Wpis nie spełnia wymagań', posts
    
