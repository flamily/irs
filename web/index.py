from flask import Blueprint, render_template

from web.decorators import templated, login_required


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
INDEX_BLUEPRINT = Blueprint('index', __name__, template_folder='templates')

@INDEX_BLUEPRINT.route('/')
@login_required()
@templated(template='index.html')
def index():
    return dict(page_title='IRS - Admin Dashboard')
