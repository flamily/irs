from flask import request, redirect, url_for

from irs.irs_app import app
from irs.irs_app.decorators import templated
from irs.irs_app.db import db


@app.route('/')
@templated()
def index():
    return redirect(url_for('friend'))


@app.route('/friend', methods=['POST'])
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
    return redirect(url_for('friend'))


@app.route('/friend', methods=['GET'])
@templated()
def friend():
    with db.cursor() as curs:
        curs.execute('select username from staff;')
        return dict(friends=curs.fetchall())
