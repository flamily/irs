from flask import Blueprint, render_template


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
LOGIN_BLUEPRINT = Blueprint('login', __name__, template_folder='templates')


@LOGIN_BLUEPRINT.route('/')
def index():
    page_title = 'Intelligent Restaurant System - Login'
    return render_template('login.html', page_title=page_title)
