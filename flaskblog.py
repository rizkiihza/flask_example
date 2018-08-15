from flask import (
    Flask,
    render_template,
    url_for, flash,
    redirect
)
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4c1813f4c3040f1550240497ed03b73'

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

    if form.validate_on_submit():
        flash('Account created for %s with email %s'
                    % (form.username.data, form.email.data), 'success')
        return redirect(url_for('home_page'))

    return render_template('register.html', title="Register", form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login successful for account %s ' % form.username.data)
        return redirect(url_for('home_page'))

    return render_template('login.html', title="Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)
