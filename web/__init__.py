"""
Exposes endpoints for satisfaction data collection from the database

Author: Robin Wohlers-Reichel, Jacob Vorreiter
Date: 13/11/2018
"""

import os
import traceback
from flask import Flask, render_template, jsonify
from web.db import register as register_db
from web.db import db
from web.login import LOGIN_BLUEPRINT
from web.index import INDEX_BLUEPRINT
from web.robot import ROBOT_BLUEPRINT
from web.tables import TABLES_BLUEPRINT
from web.reporting_api import API_BLUEPRINT, InvalidUsage
from web.orders import ORDERS_BLUEPRINT


APP = Flask(__name__)
APP.secret_key = os.environ.get("SECRET", os.urandom(16))
register_db(APP)
APP.register_blueprint(LOGIN_BLUEPRINT, url_prefix="/login")
APP.register_blueprint(INDEX_BLUEPRINT)
APP.register_blueprint(TABLES_BLUEPRINT)
APP.register_blueprint(ROBOT_BLUEPRINT)
APP.register_blueprint(API_BLUEPRINT, url_prefix="/api")
APP.register_blueprint(ORDERS_BLUEPRINT)


@APP.errorhandler(404)
def not_found(e):
    """Handle file not found error nicely"""
    print('attempt to access missing: {}'.format(e))
    return render_template('404.html'), 404


@APP.errorhandler(KeyError)
def key_error(_):
    """Handle bad key error nicely"""
    traceback.print_exc()
    db.rollback()
    return render_template('500.html'), 400


@APP.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handle API endpoint bad request nicely"""
    traceback.print_exc()
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    db.rollback()
    return response


@APP.errorhandler(Exception)
def generic_error(_):
    """Gotta catch em all."""
    # teardown_appcontext does not recieve error objects if an exception
    # handler for a specific exception is setup, as such, we need to do the
    # rollback here.
    traceback.print_exc()
    db.rollback()
    return render_template('500.html'), 500
