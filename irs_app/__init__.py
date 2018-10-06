from flask import Flask

from irs.irs_app.db import register as register_db
app = Flask(__name__)
register_db(app)

import irs.irs_app.routes
