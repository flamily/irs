from flask import Flask

from irs.web.db import register as register_db
from irs.web.login import LOGIN_BLUEPRINT

APP = Flask(__name__)
register_db(APP)


APP.register_blueprint(LOGIN_BLUEPRINT, url_prefix="/login")
