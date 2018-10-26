from flask import Blueprint

from web.decorators import templated


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
WELCOME_BLUEPRINT = Blueprint('welcome', __name__, template_folder='templates')


@WELCOME_BLUEPRINT.route('/welcome')
@templated(template='welcome.html')
def index():
    return dict(page_title='Robot - Welcome')
