from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user, current_user, login_required

from flaskblog.app import app, bcrypt, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [
    {
        'author': 'Rizki Ihza Parama',
        'title': 'Blog Post 1',
        'content': 'First Blog Post',
        'date': 'April 20, 2018'
    },
    {
        'author': 'Nadia Dewi',
        'title': 'Blog Post 2',
        'content': 'Second Blog Post',
        'date': 'April 21, 2018'
    },
]


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html', posts=posts, title='Home')


@app.route("/about/")
def about_page():
    return render_template('about.html', title='About')


@app.route("/register/", methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        try:
            form.validate_username_and_email()
            user = User(username=form.username.data,email=form.email.data,password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('your account has been created', 'success')

            return redirect(url_for('login_page'))

        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('register_page'))


    return render_template('register.html', title="Register", form=form)


@app.route("/login/", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    if form.validate_on_submit():
        if form.validate_login():
            flash('Login successful for account %s ' % form.email.data, 'success')
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user,remember=form.remember.data)

            next_page = request.args.get('next') if request.args.get('next') is not None \
                                                    else url_for('home_page')
            return redirect(next_page)
        else:
            flash('Wrong username or password', 'danger')

    return render_template('login.html', title="Login", form=form)

@app.route("/logout/")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/account/")
@login_required
def account_page():
    return render_template('account.html', title="Account")