from flask import (
    Blueprint, request
)

from web.decorators import (
    login_required, templated
)

import biz.manage_restaurant as mr


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


@ROBOT_BLUEPRINT.route('/robot/party', methods=['GET'])
@templated(template='select-party-size.html')
@login_required()
def party():
    return dict(page_title='Robot - Select Party Size')


@ROBOT_BLUEPRINT.route('/robot/table', methods=['POST', 'GET'])
@templated(template='robot-table-availability.html')
@login_required()
def tableAvailability():
    # Needs to handle response if there are no free tables.
    # Should route page to /robot/table/full
    # !! Comment out below section to test that pages work !!
    if request.method == 'POST':
        staff_id = ms.lookup_id(db, session['username'])
        table_id = int(request.form['tableId']) # This isn't implemented in the html yet so it wouldn't work
        event_id, reservation_id = mr.create_reservation(db, table_id, staff_id, group_size) # Need to grab value for group_size 
        return redirect(url_for('robot.confirmation')) # Need to map {resid} in query param
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