from flask import Blueprint
from web.decorators import (
    login_required, templated
)

# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
ROBOT_BLUEPRINT = Blueprint('robot', __name__, template_folder='templates')


@ROBOT_BLUEPRINT.route('/robot')
@templated(template='robot-welcome.html')
@login_required()
def index():
    return dict(page_title='Robot - Welcome')


@ROBOT_BLUEPRINT.route('/robot/party-size', methods=['GET'])
@templated(template='robot-select-party-size.html')
@login_required()
def party_size():
    return dict(page_title='Robot - Select Party Size')


@ROBOT_BLUEPRINT.route('/robot/table', methods=['GET'])
@templated(template='robot-table-availability.html')
@login_required()
def table_availability():
    return dict(page_title='Robot - Select Table')


@ROBOT_BLUEPRINT.route('/robot/full', methods=['GET'])
@templated(template='robot-table-full.html')
@login_required()
def table_full():
    return dict(page_title='Robot - Tables Full')


@ROBOT_BLUEPRINT.route('/robot/proceed', methods=['GET'])
@templated(template='robot-table-confirmation.html')
@login_required()
def confirmation():
    return dict(page_title='Robot - Tables Full')
