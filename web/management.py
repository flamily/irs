from flask import request, redirect, url_for, Blueprint, render_template

from irs.web.decorators import templated
from irs.web.db import db


management_blueprint = Blueprint('management', __name__, template_folder='templates')


@management_blueprint.route('/')
@templated(template='management/test.html')
def index():
    return dict(bingo='bango')
    # return render_template('management/test.html', name='bingo')
