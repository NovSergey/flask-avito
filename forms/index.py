from wtforms import SubmitField, StringField, SelectField
from flask_wtf import FlaskForm


class IndexForm(FlaskForm):
    title = StringField('Введите категорию', render_kw={"placeholder": "Название"})
    category = SelectField("Категория", choices=["Машинка", "Верталёт", "Трактор", "Грузовик", "Самолёт"])
    submit = SubmitField('Найти')