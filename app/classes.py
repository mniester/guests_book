class Post:
    
    '''Post taken from DB'''

    __slots__ = 'user', 'text', 'date'
    
    def __init__(self, data):
        self.user = data[2]
        self.text = data[1]
        self.date = data[3][:19]

    def get_text(self, cut):
        if cut:
            text = self.text.split(' ')[:cut]
            text = ' '.join(text)
            if text != self.text:
                return text + ' ...'
            return text
        else:
            return self.text
    
    def __repr__(self):
        return f'Post, {self.user}, {self.date} \n {self.get_text(10)}'
