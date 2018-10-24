"""
Flask endpoints for managing restaurant tables.

Author: Andrew Pope
Date: 22/10/2018
"""
from urllib.parse import urlparse, urljoin
from flask import (
    redirect,
    url_for, Blueprint, render_template,
    request, session
)
from web.db import db
import biz.manage_restaurant as mr
import biz.manage_staff as ms
from web.decorators import login_required, templated

# TODO: This template needs to be changed
TABLES_BLUEPRINT = Blueprint('tables', __name__, template_folder='templates')


@TABLES_BLUEPRINT.route('/tables', methods=['GET'])
@templated(template='tables.html')
@login_required()
def index():
    """Render the list of tables in the restaurant."""
    return dict(page_title='Restaurant Tables')


@TABLES_BLUEPRINT.route("/tables/pay/", methods=['POST'])
@login_required()
def pay():
    """Process a pay event, and send off exit image for processing."""
    # Lookup the staff member's id for accountability
    staff_id = ms.lookup_id(db, session['username'])  # TODO: Do we need to catch exceptions?
    # Get the table id from the request
    table_id = int(request.form['tableId'])  # TODO: What are corect naming conventions in forms?
    event_id, reservation_id = mr.paid(db, table_id, staff_id)
    # Get the exit image and send to bucket
    customer_img = request.form['customerImg']  # TODO: What format will this be??
    # TODO: Send to bucket?? (customer_img, event_id, reservation_id)
    return redirect(url_for('tables.index'))


@TABLES_BLUEPRINT.route("/tables/maintain/", methods=['POST'])
@login_required()
def maintain():
    # # Lookup the staff member's id for accountability
    # staff_id = ms.lookup_id(db, session['username'])
    # # Get the table id from the request
    # table_id = int(request.form['table_id'])
    #
    # # TODO: How do we catch exceptions that invalidate table state rules?
    # # And how to display to user?
    # mr.maintain(db, table_id, staff_id)
    #
    return redirect(url_for('tables.index'))


@TABLES_BLUEPRINT.route("/tables/ready/", methods=['POST'])
@login_required()
def ready():
    # # Lookup the staff member's id for accountability
    # staff_id = ms.lookup_id(db, session['username'])
    # # Get the table id from the request
    # table_id = int(request.form['table_id'])
    #
    # # TODO: How do we catch exceptions that invalidate table state rules?
    # # And how to display to user?
    # mr.ready(db, table_id, staff_id)
    #
    return redirect(url_for('tables.index'))
