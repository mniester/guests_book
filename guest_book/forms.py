from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length #, DataRequired



class Entry_form(FlaskForm):

    length_message = ' musi być pomiędzy %(min)d i %(max)d'
    nick_message = 'Nick' + length_message
    post_message = 'Wpis' + length_message
    
    #nick = StringField('Użytkownik', validators = [DataRequired(), Length(min = 1, max = 20, message = nick_message)])
    #text = StringField('Wpis', validators = [DataRequired(), Length(min = 1, max = 1000,  message = post_message)])
    
    nick = StringField('Użytkownik', validators = [Length(min = 1, max = 20, message = nick_message)])
    text = StringField('Wpis', validators = [Length(min = 1, max = 1000,  message = post_message)])
    submit = SubmitField('Zapisz')



class Query_form(FlaskForm):

    message = 'Zapytanie musi być pomiędzy %(min)d i %(max)d'
    #query = StringField('Zapytanie', validators = [DataRequired(), Length(min = 1, max = 1000,  message = message)])
    query = StringField('Zapytanie', validators = [Length(min = 1, max = 1000,  message = message)])
    submit = SubmitField('Szukaj')
