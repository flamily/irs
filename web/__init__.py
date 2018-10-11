from flask import Flask

from irs.web.db import register as register_db
from irs.web.friend import friend_blueprint
from irs.web.management import management_blueprint


app = Flask(__name__)
register_db(app)
app.register_blueprint(friend_blueprint)
app.register_blueprint(management_blueprint, url_prefix='/mgmt')
