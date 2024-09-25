from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from .models.user import User


class RegistrationForm(FlaskForm):
    name = StringField('ФИО',  validators=[DataRequired(), Length(min=2, max=100)])
    login = StringField('Логин',  validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Загрузите картинку', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])    
    submit = SubmitField('Зарегистрироваться')
    
    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Логин занят. Придумайте другой.')
    
    
class LoginForm(FlaskForm):    
    login = StringField('Логин', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
    
class ParticipantsForm(FlaskForm):
    participants = SelectField('participants', choices=[], render_kw={'class':'form-control'})

class OrganizerForm(FlaskForm):
    organizer = SelectField('organizer', choices=[], render_kw={'class':'form-control'}) 

# class FeedbackForm(FlaskForm):    
#     message = TextAreaField("Message", validators=[DataRequired()])
#     submit = SubmitField("Submit")    