from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, send_from_directory

import irs.irs_app.db
app = Flask(__name__)

db.register(app)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/static/js', path)

@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('templates/static/vendor', path)

@app.route('/')
def hello_world(name=None):
    return render_template('index.html', name=name)

# friends = ['rob', 'bob']

@app.route('/friend', methods=['GET', 'POST'])
def friend_post():
    if request.method == 'POST':
        if 'name' in request.form:
            # friends.append(request.form['name'])
            with db.get_db_conn().cursor() as curs:
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
        return redirect(url_for('friend_post'))
    friends = []
    with db.get_db_conn().cursor() as curs:
        curs.execute('select username from staff;')
        friends.append(curs.fetchall())
    return render_template('friend.html', friends=friends)
