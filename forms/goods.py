from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import StringField, TextAreaField, validators
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
class GoodsForm(FlaskForm):
    file = FileField('Вставте фото', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    description = TextAreaField("Содержание")
    title = StringField('Заголовок', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    category = StringField("Категория")
    submit = SubmitField('Применить')