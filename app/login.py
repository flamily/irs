# pylint: disable=unused-import
from flask import Blueprint, render_template
from flask import request, redirect, url_for  # noqa: F401

from irs.app.decorators import templated  # noqa: F401
from irs.app.db import db  # noqa: F401


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
LOGIN_BLUEPRINT = Blueprint('login', __name__, template_folder='templates')


@LOGIN_BLUEPRINT.route('/login')
def index():
    page_title = 'Intelligent Restaurant System - Login'
    return render_template('login.html', page_title=page_title)
