from flask import render_template, flash


def render_finish(back, entry, title, query, posts, cut, status_code, message, db, quantity):
    
    '''Ends function.'''
    
    flash(message)
    
    if not posts:
        posts = db.get_posts(quantity = quantity)
        
    return render_template('index.html', back = back,
                                   entry = entry, 
                                   title = title,
                                   posts = posts,
                                   query = query,
                                   cut = cut), status_code



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



def post_method_handling(post, query, db, quantity):
    
    '''Common funtion to handle post method'''
    
    if post.validate_on_submit():
        result = add_post(post, db)
        if result:
            status_code = 201
            message = 'Twój wpis został dodany'
        else:
            pass
            #status_code = 205
            #message = 'Wpis nie spełnia wymagań'
        #return status_code, message, posts
    elif query.validate_on_submit():
        posts = search_query(query, db)
        if posts:
            status_code = 201
            message = 'Wyniki wyszukiwania'
        else:
            status_code = 204
            message = 'Nic nie znaleziono'
        print('DRY 66', status_code, message)
        return status_code, message, posts
    posts = db.get_posts(quantity = quantity)
    return 205, 'Wpis nie spełnia wymagań', posts
    
