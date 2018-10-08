from flask import request, redirect, url_for, Blueprint

from irs.irs_app.decorators import templated
from irs.irs_app.db import db


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
friend_blueprint = Blueprint('friend', __name__, template_folder='templates')


@friend_blueprint.route('/')
def index():
    return redirect(url_for('.friend'))


@friend_blueprint.route('/friend', methods=['POST'])
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
    return redirect(url_for('.friend'))


@friend_blueprint.route('/friend', methods=['GET'])
@templated()
def friend():
    with db.cursor() as curs:
        curs.execute('select username from staff;')
        return dict(friends=curs.fetchall())
