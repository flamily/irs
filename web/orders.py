from flask import (
    Blueprint, request
)
import biz.manage_restaurant as mr
import biz.manage_menu as mm
from web.db import db
from web.decorators import (
    login_required, templated, user
)

ORDERS_BLUEPRINT = Blueprint('order', __name__, template_folder='templates')


@ORDERS_BLUEPRINT.route('/order/tables', methods=['GET'])
@login_required()
@templated(template='order-table.html')
def get_occupied_tables():
    tables = mr.overview(db)
    occupied_tables = list()
    for table in tables:
        if mr.lookup_reservation(db, table.rt_id):
            occupied_tables.append(table)
    return dict(page_title='Order - Select Table',
                tables=occupied_tables)


@ORDERS_BLUEPRINT.route('/order/new', methods=['GET'])
@login_required()
def get_order():
    table_id = request.json['table_id']
    rid = mr.lookup_reservation(db, table_id)
    if not rid:
        return "No reservation found for table: " + table_id

    return str(user.s_id)


@ORDERS_BLUEPRINT.route('/order/new', methods=['POST'])
@login_required()
def create_order():
    
    return str(request.json)
