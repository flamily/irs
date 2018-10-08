from flask import Flask

from irs.web.db import register as register_db
from irs.web.friend import friend_blueprint


app = Flask(__name__)
register_db(app)
app.register_blueprint(friend_blueprint)
