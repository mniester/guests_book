from guest_book import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Length, NumberRange



class Entry(FlaskForm):

    length_message = ' musi być pomiędzy %(min)d i %(max)d'
    nick_message = 'Długość nicku' + length_message
    post_message = 'Długość wpis' + length_message
    
    nick = StringField('Użytkownik', validators = [Length(min = 1, max = 20, message = nick_message)])
    text = StringField('Wpis', validators = [Length(min = 1, max = 1000,  message = post_message)])
    write = SubmitField('Zapisz')



class Query(FlaskForm):

    message = 'Zapytanie musi być pomiędzy %(min)d i %(max)d'

    query = StringField('Zapytanie o wpis', validators = [Length(min = 1, max = 1000,  message = message)])
    ask = SubmitField('Szukaj')



class Set_nr(FlaskForm):

    message = 'Liczba musi być od 1 do 100'

    nr = IntegerField('Podaj liczbę od 1 do 100', validators = [NumberRange(min = 1, max = 100,  message = message)])
    confirm = SubmitField('Ustaw')
