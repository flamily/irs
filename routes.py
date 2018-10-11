from flask import Flask, render_template

APP = Flask(__name__)


@APP.route('/')
def index():
    page_title = 'IRS - Dashboard'
    return render_template('index.html', **locals())


@APP.route('/login')
def login():
    page_title = 'Intelligent Restaurant System - Login'
    return render_template('login.html')


@APP.route('/users')
def users():
    page_title = 'IRS - Users'
    return render_template('tables.html')


@APP.route('/reports')
def reports():
    page_title = 'IRS - Reports'
    return render_template('charts.html')


@APP.route('/error-404')
def error():
    page_title = 'SB Admin - 404 Error'
    return render_template('404.html')
