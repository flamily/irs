from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, send_from_directory


import irs.irs_app.db
app = Flask(__name__)

db.register(app)

import irs.irs_app.routes
