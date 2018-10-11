# pylint: disable=unused-import
from flask import Blueprint
from flask import request, redirect, url_for, render_template  # noqa: F401

from irs.app.decorators import templated  # noqa: F401
from irs.app.db import db  # noqa: F401

USER_BLUEPRINT = Blueprint('user', __name__, template_folder='templates')


@USER_BLUEPRINT.route('/login')
def login():
    return render_template("login.html")
