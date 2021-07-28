class Entry:

    '''Entry taken from DB'''

    __slots__ = 'id', 'user', 'text', 'date'

    def __init__(self, data):
        self.id = data[0]
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
        return f'Entry, {self.user}, {self.date} \n {self.get_text(10)}\n\n'
