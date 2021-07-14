class Post:

    __slots__ = 'user', 'text', 'date'
    
    def __init__(self, data):
        self.user = data[2]
        self.text = data[1]
        self.date = data[3]
    
    def get_excerpt(self, x):
        return self.text[:x]
