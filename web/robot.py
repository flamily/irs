from flask import (
    Blueprint, request, url_for, redirect, render_template
)
import biz.manage_restaurant as mr
from biz.css.file_storage import bucket_upload
from web.db import db
from web.decorators import (
    login_required, templated, user
)


ROBOT_BLUEPRINT = Blueprint('robot', __name__, template_folder='templates')


@ROBOT_BLUEPRINT.route('/robot')
@login_required()
def index():
    tables = mr.get_available_tables(db, 0)
    if not tables:
        return redirect(url_for('robot.table_full'))
    return render_template('robot-welcome.html')


@ROBOT_BLUEPRINT.route('/robot/party', methods=['GET'])
@templated(template='robot-select-party-size.html')
@login_required()
def party_size():
    return dict(page_title='Robot - Select Party Size')


@ROBOT_BLUEPRINT.route('/robot/table', methods=['GET'])
@login_required()
def table():
    people = int(request.args.get('people', '999'))
    tables = mr.get_available_tables(db, people)
    if not tables:
        return redirect(url_for('robot.table_full'))
    tables = mr.overview(db)
    return render_template(
        'robot-table-availability.html',
        tables=tables,
        people=people
    )


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
    return redirect(
        url_for(
            'robot.confirmation',
            rid=rid,
            tid=table_id,
            group_size=group_size
        )
    )


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
    group_size = request.args.get('group_size', 'NO_GROUP_SIZE')
    return dict(
        page_title='Robot - Tables Full',
        table=tid,
        rid=rid,
        group_size=group_size
    )
