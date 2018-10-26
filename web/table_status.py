from flask import Blueprint

from web.decorators import templated

TABLE_STATUS_BLUEPRINT = Blueprint(
    'table_status', __name__, template_folder='templates')


@TABLE_STATUS_BLUEPRINT.route('/table-status')
@templated(template='table-status.html')
def index():
    return dict(page_title='IRS - Table Status')
