from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home_page():
    return "<h1>Home Page</h1>"


@app.route("/about/")
def about_page():
    return "<h1>About Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)
