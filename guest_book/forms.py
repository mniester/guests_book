from guest_book import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Length, NumberRange
from wtforms.widgets import TextArea



max_nick_len = 20
max_entry_len = 1000



class Entry(FlaskForm):

    length_message = ' musi być pomiędzy %(min)d i %(max)d'
    nick_message = 'Długość nicku' + length_message
    entry_message = 'Długość wpisu' + length_message
    nick_placeholder = f'Max. {max_nick_len} znaków' 
    entry_placeholder = f'Max. {max_entry_len} znaków'
    
    nick = StringField('Użytkownik', validators = [Length(min = 1, max = max_nick_len, message = nick_message)])
    text = StringField('Wpis', validators = [Length(min = 1, max = max_entry_len,  message = entry_message)], widget=TextArea())
    write = SubmitField('Zapisz')



class Query(FlaskForm):


    entry_message = 'Zapytanie musi mieć od %(min)d do %(max)d znaków'
    entry = StringField('Zapytanie o wpis', validators = [Length(min = 1, max = max_entry_len,  message = entry_message)], widget=TextArea())
    ask = SubmitField('Szukaj')
