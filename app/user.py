from flask import request, redirect, url_for, Blueprint, render_template

from irs.app.decorators import templated
from irs.app.db import db

user_blueprint = Blueprint('user', __name__, template_folder='templates')


@user_blueprint.route('/login')
def login():
	return render_template("login.html")