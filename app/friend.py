from flask import request, redirect, url_for, Blueprint
import irs.app.manage_staff as smanager
from irs.app.staff import Permission
from irs.app.decorators import templated
from irs.app.db import db


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
friend_blueprint = Blueprint('friend', __name__, template_folder='templates')


@friend_blueprint.route('', methods=['POST'])
def friend_post():
    if 'name' in request.form:
        with db.cursor() as curs:
            curs.execute(
                "INSERT INTO staff "
                "(username, password, first_name, last_name, permission) "
                "values (%s, %s, %s, %s, %s)",
                (
                    request.form['name'],
                    'password',
                    'george',
                    'Costanza',
                    'management'
                )
            )
    return redirect(url_for('.friend_get'))


@friend_blueprint.route('', methods=['GET'])
@templated(template='friend/friend.html')
def friend_get():
    with db.cursor() as curs:
        curs.execute('select username from staff;')
        return dict(friends=curs.fetchall())
        smanager.create_staff_member(
            db, request.form['name'], 'password', ('Larry', 'David'),
            Permission.management
        )
    return redirect(url_for('.friend'))


@friend_blueprint.route('/friend', methods=['GET'])
@templated()
def friend():
    usernames = [member.username for member in smanager.list_members(db)]
    return dict(friends=usernames)
