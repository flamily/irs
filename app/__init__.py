import os
from flask import Flask

from irs.app.db import register as register_db
from irs.app.friend import friend_blueprint
from irs.app.login import login_blueprint
from irs.app.index import index_blueprint


app = Flask(__name__)
app.secret_key = os.urandom(16)

register_db(app)
app.register_blueprint(friend_blueprint, url_prefix="/friend")
app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(index_blueprint)
