from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length
from wtforms.widgets import TextArea


max_entry_len = 1000


class Entry(FlaskForm):

    max_user_len = 20
    length_message = ' musi być pomiędzy %(min)d i %(max)d'
    user_message = 'Długość useru' + length_message
    entry_message = 'Długość wpisu' + length_message
    query_message = 'Długośc zapytania' + length_message
    user_placeholder = f'Max. {max_user_len} znaków' 
    entry_placeholder = f'Max. {max_entry_len} znaków'
    user = StringField('Użytkownik', validators = [Length(min = 1, 
        max = max_user_len, message = user_message)])
    text = StringField('Wpis', validators = [Length(min = 1,
        max = max_entry_len,  message = entry_message)], widget=TextArea())
    write = SubmitField('Zapisz wpis')
    query = SubmitField('Szukaj wpisu')
