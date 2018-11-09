import os
from flask import Flask, render_template
from web.db import register as register_db
from web.db import db
from web.login import LOGIN_BLUEPRINT
from web.index import INDEX_BLUEPRINT
from web.robot import ROBOT_BLUEPRINT
from web.tables import TABLES_BLUEPRINT
from web.robot import ROBOT_BLUEPRINT


APP = Flask(__name__)
APP.secret_key = os.environ.get("SECRET", os.urandom(16))
register_db(APP)
APP.register_blueprint(LOGIN_BLUEPRINT, url_prefix="/login")
APP.register_blueprint(INDEX_BLUEPRINT)
APP.register_blueprint(TABLES_BLUEPRINT)
APP.register_blueprint(ROBOT_BLUEPRINT)


@APP.errorhandler(404)
def not_found(e):
    print('attempt to access missing: {}'.format(e))
    return render_template('404.html'), 404


@APP.errorhandler(KeyError)
def key_error(e):
    print('KeyError: {}'.format(e))
    db.rollback()
    return render_template('500.html'), 400
