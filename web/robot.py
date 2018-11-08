from flask import (
    Blueprint, request, url_for, redirect
)
import biz.manage_restaurant as mr
from biz.css.file_storage import bucket_upload
from web.db import db
from web.decorators import (
    login_required, templated, user
)


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
def table():
    people = int(request.args.get('people', '999'))
    tables = mr.overview(db)
    return dict(page_title='Robot - Select Table',
                tables=tables,
                people=people)


@ROBOT_BLUEPRINT.route('/robot/table/reserve', methods=['POST'])
@login_required()
def reserve_table():
    # if all the parameters are correct, we redirect to proceed
    # if any of the parameters are incorrect, we redirect back to start
    table_id = request.form['table_id']
    group_size = request.form['group_size']
    photo = request.form['photo']
    eid, rid = mr.create_reservation(db, table_id, user.s_id, group_size)
    bucket_upload(photo, eid, rid)
    return redirect(url_for('robot.confirmation', rid=rid, tid=table_id))


@ROBOT_BLUEPRINT.route('/robot/full', methods=['GET'])
@templated(template='robot-table-full.html')
@login_required()
def table_full():
    return dict(page_title='Robot - Tables Full')


@ROBOT_BLUEPRINT.route('/robot/proceed', methods=['GET'])
@templated(template='robot-table-confirmation.html')
@login_required()
def confirmation():
    tid = request.args.get('tid', 'NO_TABLE_ID')
    rid = request.args.get('rid', 'NO_RESERVATION_ID')
    return dict(page_title='Robot - Tables Full', table=tid, rid=rid)
