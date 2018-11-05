from flask import (
    Blueprint
)
from web.decorators import (
    login_required, templated
)


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
ROBOT_BLUEPRINT = Blueprint('robot', __name__, template_folder='templates')


@ROBOT_BLUEPRINT.route('/robot')
@templated(template='welcome.html')
@login_required()
def index():
    return dict(page_title='Robot - Welcome')


@ROBOT_BLUEPRINT.route('/robot/listen', methods=['GET'])
@templated(template='robot-listening.html')
@login_required()
def listen():
    return dict(page_title='Robot - Welcome')


@ROBOT_BLUEPRINT.route('/robot/party', methods=['GET', 'POST'])
@templated(template='select-party-size.html')
@login_required()
def party():
    return dict(page_title='Robot - Select Party Size')


@ROBOT_BLUEPRINT.route('/robot/tables', methods=['GET'])
@templated(template='robot-table-availability.html')
@login_required()
def tableAvailability():
    return dict(page_title='Robot - Select Table')