import phonenumbers
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, TelField , EmailField, BooleanField
from wtforms.validators import DataRequired, ValidationError


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    phone = TelField('Телефон', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class EditEmailForm(FlaskForm):
    email = EmailField('Новая почта', validators=[DataRequired()])
    submit = SubmitField('Изменить')

class EditPhoneForm(FlaskForm):
    submit = SubmitField('Изменить')
    phone = TelField('Телефон', validators=[DataRequired()])
    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
class EditPasswordForm(FlaskForm):
    password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')
