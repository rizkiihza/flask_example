from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('username',
                    validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('email',
                    validators=[DataRequired(), Email()])
    password = PasswordField('password',
                    validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confirm_password',
                    validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('email',
                    validators=[DataRequired(), Email()])
    password = PasswordField('password',
                    validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')

