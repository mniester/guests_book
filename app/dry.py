from flask import render_template



def render_finish(post, title, query, posts, cut, status_code):
    
    '''Ends function.'''
        
    return render_template('index.html', post = post, 
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
    
    data = query.text.data
    posts = db.get_posts(query = data)
    posts = list(posts)
    return posts



def post_method_handling(post, query, db, quantity):
    
    '''Common funtion to handle post method'''
    
    def inner(post, query, db):
    
        if post.validate_on_submit():
            result = add_post(post, db)
            if result:
                status_code = 201
                message = 'Twój wpis został dodany'
            else:
                status_code = 205
                message = 'Wpis nie spełnia wymagań'
            return status_code, message
        elif query.validate_on_submit():
            posts = search_query(query, db)
            if posts:
                status_code = 201
                message = 'Wyniki wyszukiwania'
            else:
                status_code = 204
                message = 'Nic nie znaleziono'
            return status_code, message, posts
        return None
    
    result = inner(post, query, db)
    if result:
        try:
            status_code, message, posts = result
        except ValueError:
            status_code, message = result
            posts = db.get_posts(quantity = quantity)
    else:
        status_code = 400
        message = 'Twój wpis został odrzucony'
    return status_code, message, posts
        #return render_finish(post, title, query, posts, cut, status_code)
    
