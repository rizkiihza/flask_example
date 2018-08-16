from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flaskblog.models import User
from flaskblog.app import bcrypt

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

    def validate_username_and_email(self):
        user = User.query.filter_by(username=self.username.data).all() + \
                    User.query.filter_by(email=self.email.data).all()

        if len(user) > 0:
            raise Exception('user already exist')

class LoginForm(FlaskForm):
    email = StringField('email',
                    validators=[DataRequired(), Email()])
    password = PasswordField('password',
                    validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')

    def validate_login(self):
        user = User.query.filter_by(email=self.email.data).first()

        return user is not None and \
               bcrypt.check_password_hash(user.password, self.password.data)

