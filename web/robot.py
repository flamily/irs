from flask import Blueprint

from web.decorators import templated, login_required


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
ROBOT_BLUEPRINT = Blueprint('robot', __name__, template_folder='templates')


@ROBOT_BLUEPRINT.route('/robot/tables')
@templated(template='robot-tables.html')
@login_required()
def tables():
    return dict(page_title='Robot- Select Tables')
