from wtforms import SubmitField, StringField
from flask_wtf import FlaskForm


class IndexForm(FlaskForm):
    title = StringField('Введите категорию')
    submit = SubmitField('Найти')