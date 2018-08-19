from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import current_user

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

class UpdateAccountForm(FlaskForm):
    username = StringField('username',
                    validators=[DataRequired(), Length(8)])
    email = StringField('email',
                    validators=[DataRequired()])
    password = PasswordField('password',
                    validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('password',
                    validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_username_and_email(self):
        if self.email != current_user.email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise Exception('user with email %s already exist' % self.email)

        if self.username != current_user.username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise Exception('user with username %s already exist' % self.username)