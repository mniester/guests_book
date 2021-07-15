class Post:
    
    '''Post taken from DB '''

    __slots__ = 'user', 'text', 'date'
    
    def __init__(self, data):
        self.user = data[2]
        self.text = data[1]
        self.date = data[3]
    
    def get_excerpt(self, x):
        excerpt = self.text.split(' ')[:x]
        excerpt = ' '.join(excerpt)
        if excerpt != self.text:
            return excerpt + ' ...'
        return excerpt
    
    def __repr__(self):
        return f'Post, {self.user}, {self.date} \n {self.get_excerpt(10)}'
