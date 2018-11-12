from flask import Blueprint, request, jsonify

from web.reporting import *


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
API_BLUEPRINT = Blueprint('api', __name__, template_folder='templates')

@API_BLUEPRINT.route('/reporting/Customer/<type>')
def get_customer_report(type):
    date_string = request.args.get('dateString')

    res = get_customer_satisfaciton(type, date_string)
    labels, data = get_chart_data(res)
    avg = get_average_score(type, date_string)

    return jsonify(data=res, labels=labels, scores=data, average=avg)

@API_BLUEPRINT.route('/reporting/Staff/<id>/<date_type>')
def get_staff_report(id, date_type):
    date_string = request.args.get('dateString')

    res = get_staff_satisfaction_report(id, date_type, date_string)
    labels, data = get_chart_data(res)
    avg = get_staff_average_score(id, date_type, date_string)

    return jsonify(data=res, labels=labels, scores=data, average=avg)

@API_BLUEPRINT.route('/reporting/Menu/<id>/<date_type>')
def get_menu_score(id, date_type):
    date_string = request.args.get('dateString')
    res = get_menu_satisfaction(id, date_type, date_string)
    labels, scores = get_chart_data(res)
    avg = get_avg_menu_score(id, date_type, date_string)

    return jsonify(data=res, labels=labels, scores=scores, average=avg)

@API_BLUEPRINT.route('/reporting/list_items')
def get_staff_and_menu_items():
    staff_list = get_staff_members()
    menu_list = get_menu_items()

    return jsonify(menu=menu_list, staff=staff_list)

@API_BLUEPRINT.route('/time/get_latest')
def get_latest_entry_time():
    time = get_latest_time()

    return jsonify(data=time)

@API_BLUEPRINT.route('/time/get_years')
def get_list_of_years():
    time = get_year_list()

    return jsonify(years=time)
