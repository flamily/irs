from flask import Flask, render_template

APP = Flask(__name__)


@APP.route('/')
def index():
    page_title = 'IRS - Dashboard'
    breadcrumb_title = ''
    return render_template(
        'index.html',
        page_title=page_title,
        breadcrumb_title=breadcrumb_title
    )


@APP.route('/login')
def login():
    page_title = 'Intelligent Restaurant System - Login'
    return render_template('login.html', page_title=page_title)


@APP.route('/users')
def users():
    page_title = 'IRS - Users'
    breadcrumb_title = 'Users'
    return render_template(
        'tables.html',
        page_title=page_title,
        breadcrumb_title=breadcrumb_title
    )


@APP.route('/reports')
def reports():
    page_title = 'IRS - Reports'
    breadcrumb_title = 'Reports'
    return render_template(
        'charts.html',
        page_title=page_title,
        breadcrumb_title=breadcrumb_title
    )


@APP.route('/error-404')
def error():
    page_title = 'IRS - 404 Error'
    breadcrumb_title = 'Error'
    return render_template(
        '404.html',
        page_title=page_title,
        breadcrumb_title=breadcrumb_title
    )
