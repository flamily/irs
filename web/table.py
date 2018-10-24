from flask import Blueprint

from web.decorators import templated

TABLE_BLUEPRINT = Blueprint('table', __name__, template_folder='templates')


@TABLE_BLUEPRINT.route('/table')
@templated(template='update-table-status.html')
def index():
    return dict(page_title='Table')

