from flask import (
    Blueprint, request, jsonify
)
import biz.manage_restaurant as mr
import biz.manage_menu as mm
from web.db import db
from web.decorators import (
    login_required, templated, user
)

ORDERS_BLUEPRINT = Blueprint('order', __name__, template_folder='templates')


@ORDERS_BLUEPRINT.route('/order/new', methods=['GET'])
@login_required()
@templated(template='order-new.html')
def get_occupied_tables():
    menu_items = mm.list_menu(db)
    tables = mr.overview(db)
    occupied_tables = list()
    for table in tables:
        if mr.lookup_reservation(db, table.rt_id):
            occupied_tables.append(table)
    return dict(page_title='Order - Select Table',
                tables=occupied_tables,
                menu_items=menu_items)


@ORDERS_BLUEPRINT.route('/order/new', methods=['POST'])
@login_required()
@templated(template='order-created.html')
def create_order():
    menu_items = list()
    for value in request.form:
        if value == "table_id":
            table_id = request.form[value]
        else:
            if request.form[value]:
                menu_item = tuple([int(value), int(request.form[value])])
                menu_items.append(menu_item)
    eid, rid, oid = mr.order(db, menu_items, table_id, user.s_id)
    return dict(page_title='Order - Created',
                eid=eid,
                rid=rid,
                oid=oid)


@ORDERS_BLUEPRINT.route('/order/get', methods=['GET'])
@login_required()
def get_order():
    rid = request.args['rid']
    response = mr.lookup_order(db, rid)
    return jsonify(response)
