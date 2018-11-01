from flask import Blueprint

from web.decorators import (
    login_required, templated
)


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
SELECT_PARTY_SIZE_BLUEPRINT = Blueprint(
    'select_party_size', __name__, template_folder='templates')


@SELECT_PARTY_SIZE_BLUEPRINT.route('/select-party-size', methods=['GET'])
@templated(template='select-party-size.html')
@login_required()
def index():
    return dict(page_title='Robot - Select Party Size')
