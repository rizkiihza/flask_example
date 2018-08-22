from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
import os

from flaskblog.app import app, bcrypt, db
from flaskblog.forms import (
    RegistrationForm, 
    LoginForm, 
    UpdateAccountForm,
    PostForm
)
from flaskblog.models import User, Post
from flaskblog.task.user_account import save_picture


@app.route("/")
@app.route("/home")
def home_page():
    posts = Post.query.all()
    return render_template('home.html', posts=posts, title='Home')

@app.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post_page():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        post.author_id = current_user.id
        db.session.add(post)
        db.session.commit()
        flash("post successfully created", "success")
        return redirect(url_for('home_page'))

    return render_template('create_post.html', form=form, title='Create Post')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_page(post_id):
    post = Post.query.get(post_id)
    form = PostForm()

    if form.validate_on_submit():
        post = Post.query.get(post_id)
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("post have been edited successfully", "success")
        return redirect(url_for('home_page'))

    if request.method == 'GET':
        form.content.data = post.content
        form.title.data = post.title

    return render_template('edit_post.html', post=post, form=form, title='Edit Post')

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

@app.route("/account/", methods=['GET', 'POST'])
@login_required
def account_page():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        try:
            form.validate_username_and_email()
            if form.password.data != form.confirm_password.data:
                raise Exception('password typed are different')

            user = User.query.filter_by(username=current_user.username, email=current_user.email).first()
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.username = form.username.data
            user.email = form.email.data
            user.password = hashed_password

            if form.image_file:
                picture_name = save_picture(form.image_file.data)
                user.image_file = picture_name

            db.session.commit()
            flash('Your account has been changed', 'success')
            login_user(user)
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('account_page'))


    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", form=form, image_file=image_file)  