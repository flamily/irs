<< << << < HEAD
from flask import (
    Blueprint
)
== == == =
from flask import Blueprint
>>>>>> > master
from web.decorators import (
    login_required, templated
)

<< << << < HEAD
# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
== == == =

>>>>>> > master
ROBOT_BLUEPRINT = Blueprint('robot', __name__, template_folder='templates')


@ROBOT_BLUEPRINT.route('/robot')
<< << << < HEAD


@templated(template='welcome.html')
== == == =


@templated(template='robot-welcome.html')
>>>>>> > master


@login_required()
def index():
    return dict(page_title='Robot - Welcome')


<< << << < HEAD


@ROBOT_BLUEPRINT.route('/robot/party-size', methods=['GET'])
@templated(template='select-party-size.html')
@login_required()
def party():
    return dict(page_title='Robot - Select Party Size')


== == == =


@ROBOT_BLUEPRINT.route('/robot/party', methods=['GET'])
@templated(template='robot-select-party-size.html')
@login_required()
def party():
    return dict(page_title='Robot - Select Party Size')


@ROBOT_BLUEPRINT.route('/robot/table', methods=['GET'])
@templated(template='robot-table-availability.html')
@login_required()
def tableAvailability():
    return dict(page_title='Robot - Select Table')


@ROBOT_BLUEPRINT.route('/robot/full', methods=['GET'])
@templated(template='robot-table-full.html')
@login_required()
def tableFull():
    return dict(page_title='Robot - Tables Full')


@ROBOT_BLUEPRINT.route('/robot/proceed', methods=['GET'])
@templated(template='robot-table-confirmation.html')
@login_required()
def confirmation():
    return dict(page_title='Robot - Tables Full')


>>>>>> > master
