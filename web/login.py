from urllib.parse import urlparse, urljoin
from flask import (
    redirect,
    url_for, Blueprint, render_template,
    request, session
)


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


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


@LOGIN_BLUEPRINT.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['email']
        return redirect_back('index.index')
    next = get_redirect_target()
    return render_template('login.html', next=next)


@LOGIN_BLUEPRINT.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index.index'))
