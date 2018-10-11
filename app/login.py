from flask import request, redirect, url_for, Blueprint, render_template

from irs.app.decorators import templated
from irs.app.db import db


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
login_blueprint = Blueprint('login', __name__, template_folder='templates')


@login_blueprint.route('')
def index():
    return render_template('login.html')