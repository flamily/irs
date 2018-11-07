"""
Flask endpoints for managing restaurant tables.

Author: Andrew Pope
Date: 22/10/2018
"""
from flask import (
    Blueprint, request, jsonify
)
from web.db import db
from web.decorators import (
    login_required, templated, user
)
import biz.manage_restaurant as mr

TABLES_BLUEPRINT = Blueprint('tables', __name__, template_folder='templates')

# NB: List of tasks that need to be considered
#  - In '/tables/pay' we need to get an image from the form request and send
#    it to the 'bucket' for later CSS processing.
#  - In the template 'tables.html' we need to:
#       1. Make it pretty.
#       2. Get it to capture an image with Jason's js library.


def __mock_bucket_send(img, event_id, reservation_id):
    """Send image to bucket (mock)."""
    print("Sent ({}, {}): {}".format(event_id, reservation_id, img))


@TABLES_BLUEPRINT.route('/tables', methods=['GET'])
@templated(template='tables.html')
@login_required()
def index():
    """Render the list of tables in the restaurant."""
    table_list = mr.overview(db)
    return dict(page_title='Restaurant Tables', tables=table_list)


@TABLES_BLUEPRINT.route("/tables/pay/", methods=['POST'])
@login_required()
def pay():
    """Process a pay event, and send off exit image for processing."""
    # Get the table id from the request, and 'pay for the table'
    table_id = int(request.form['tableId'])
    event_id, reservation_id = mr.paid(db, table_id, user.s_id)

    # Get the exit image and send to bucket
    customer_img = request.form['customerImg']
    __mock_bucket_send(customer_img, event_id, reservation_id)

    return jsonify(status='unavailable')


@TABLES_BLUEPRINT.route("/tables/maintain/", methods=['POST'])
@login_required()
def maintain():
    """Mark a table for maintainence."""
    table_id = int(request.form['tableId'])
    mr.maintain(db, table_id, user.s_id)

    return jsonify(status='unavailable')


@TABLES_BLUEPRINT.route("/tables/ready/", methods=['POST'])
@login_required()
def ready():
    """Mark a table as ready."""
    table_id = int(request.form['tableId'])
    mr.ready(db, table_id, user.s_id)

    return jsonify(status='available')
