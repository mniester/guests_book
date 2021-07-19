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

    entry_message = 'Zapytanie musi być pomiędzy %(min)d i %(max)d'
    entry = StringField('Zapytanie o wpis', validators = [Length(min = 1, max = 1000,  message = entry_message)])
    ask = SubmitField('Szukaj')



class Find_user(FlaskForm):

    query_message = 'Zapytanie musi być pomiędzy %(min)d i %(max)d'
    who = StringField('Zapytanie o użytkownika', validators = [Length(min = 1, max = 20,  message = query_message)])
    find = SubmitField('Szukaj')



class Set_nr(FlaskForm):

    message = 'Liczba musi być pomiędzy %(min)d i %(max)d'
    nr = IntegerField('Liczba wyświetlanych wpisów', validators = [NumberRange(min = 1, max = 20,  message = message)])
    confirm = SubmitField('Ustaw')
