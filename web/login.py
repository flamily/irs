"""
Authentication for IRS access.

Author: Robin Wohlers-Reichel, Andrew Pope
Date: 06/11/2018
"""
from urllib.parse import urlparse, urljoin
from flask import (
    redirect,
    url_for, Blueprint, render_template,
    request, session
)

from biz import manage_staff as ms
from web.db import db


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
LOGIN_BLUEPRINT = Blueprint('login', __name__, template_folder='templates')


# from: http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
    return None


def redirect_back(endpoint, **values):
    target = request.form.get('next', None)
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


@LOGIN_BLUEPRINT.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        is_okay, login_error = __check_login_parameters(username, password)

        if not is_okay:
            return render_template(
                'login.html', next=None, error=login_error
            ), 401

        session['username'] = username
        return redirect_back('index.index')

    next_url = get_redirect_target()
    return render_template('login.html', next=next_url)


@LOGIN_BLUEPRINT.route("/logout/", methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index.index'))


def __check_login_parameters(username, password):
    if not username:
        return (False, 'Username cannot be empty')
    if not password:
        return (False, 'Password cannot be empty')
    if not ms.lookup_id(db, username):
        return (False, 'User does not exist')
    if not ms.verify_password(db, username, password):
        return (False, 'Invalid password for username')

    return (True, 'okay')
