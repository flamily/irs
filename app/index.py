from flask import Blueprint

from irs.app.decorators import templated, login_required


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
index_blueprint = Blueprint('index', __name__, template_folder='templates')


@index_blueprint.route('/')
@login_required()
@templated(template='index.html')
def index():
    return dict(page_title='bingo')
