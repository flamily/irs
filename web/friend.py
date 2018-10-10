import irs.app.manage_staff as smanager
from irs.app.staff import Permission
from flask import request, redirect, url_for, Blueprint

from irs.web.decorators import templated
from irs.web.db import db


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
friend_blueprint = Blueprint('friend', __name__, template_folder='templates')


@friend_blueprint.route('/')
def index():
    return redirect(url_for('.friend'))


@friend_blueprint.route('/friend', methods=['POST'])
def friend_post():
    if 'name' in request.form:
        smanager.create_staff_member(
            db, request.form['name'], 'password', ('Larry', 'David'),
            Permission.management
        )
    return redirect(url_for('.friend'))


@friend_blueprint.route('/friend', methods=['GET'])
@templated()
def friend():
    usernames = [member.username for member in smanager.list(db)]
    return dict(friends=usernames)
