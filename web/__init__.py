import os
from flask import Flask

from web.db import register as register_db
from web.login import LOGIN_BLUEPRINT
from web.index import INDEX_BLUEPRINT
from web.table_status import TABLE_STATUS_BLUEPRINT

APP = Flask(__name__)
APP.secret_key = os.urandom(16)
register_db(APP)
APP.register_blueprint(LOGIN_BLUEPRINT, url_prefix="/login")
APP.register_blueprint(INDEX_BLUEPRINT)
APP.register_blueprint(TABLE_STATUS_BLUEPRINT)
