from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/users')
def users():
    return render_template('tables.html')


@app.route('/reports')
def reports():
    return render_template('charts.html')


@app.route('/error-404')
def error():
    return render_template('404.html')
