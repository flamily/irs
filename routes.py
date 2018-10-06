from flask import Flask, render_template

APP = Flask(__name__)


@APP.route('/')
def index():
    return render_template('index.html')


@APP.route('/login')
def login():
    return render_template('login.html')


@APP.route('/users')
def users():
    return render_template('tables.html')


@APP.route('/reports')
def reports():
    return render_template('charts.html')


@APP.route('/error-404')
def error():
    return render_template('404.html')
