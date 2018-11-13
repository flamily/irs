from flask import Blueprint, request, jsonify

from web import reporting as report


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


API_BLUEPRINT = Blueprint('api', __name__, template_folder='templates')


@API_BLUEPRINT.route('/reporting/Customer/<date_type>')
def get_customer_report(date_type):
    date_string = request.args.get('dateString')

    if not date_string:
        raise InvalidUsage("No date string provided")

    if date_type not in ["date", "week", "month", "year"]:
        raise InvalidUsage("Invalid date format provided")

    res = report.get_customer_satisfaciton(date_type, date_string)
    labels, data = report.get_chart_data(res)
    avg = report.get_average_score(date_type, date_string)

    return jsonify(data=res, labels=labels, scores=data, average=avg)


@API_BLUEPRINT.route('/reporting/Staff/<staff_id>/<date_type>')
def get_staff_report(staff_id, date_type):
    date_string = request.args.get('dateString')

    if not date_string:
        raise InvalidUsage("No date string provided")

    if date_type not in ["date", "week", "month", "year"]:
        raise InvalidUsage("Invalid date format provided")

    if not staff_id.isdigit():
        raise InvalidUsage("Invalid staff_id provided")

    res = report.get_staff_satisfaction_report(
        staff_id,
        date_type,
        date_string)
    labels, data = report.get_chart_data(res)
    avg = report.get_staff_average_score(staff_id, date_type, date_string)

    return jsonify(data=res, labels=labels, scores=data, average=avg)


@API_BLUEPRINT.route('/reporting/Menu/<menu_id>/<date_type>')
def get_menu_score(menu_id, date_type):
    date_string = request.args.get('dateString')

    if not date_string:
        raise InvalidUsage("No date string provided")

    if date_type not in ["date", "week", "month", "year"]:
        raise InvalidUsage("Invalid date format provided")

    if not menu_id.isdigit():
        raise InvalidUsage("Invalid menu_id provided")

    res = report.get_menu_satisfaction(menu_id, date_type, date_string)
    labels, scores = report.get_chart_data(res)
    avg = report.get_avg_menu_score(menu_id, date_type, date_string)

    return jsonify(data=res, labels=labels, scores=scores, average=avg)


@API_BLUEPRINT.route('/reporting/Staff//<date_type>')
def staff_missing_error(date_type):
    # pylint: disable=unused-argument
    raise InvalidUsage("Missing staff_id from request")


@API_BLUEPRINT.route('/reporting/Menu//<date_type>')
def menu_missing_error(date_type):
    # pylint: disable=unused-argument
    raise InvalidUsage("Missing menu_id from request")


@API_BLUEPRINT.route('/reporting/list_items')
def get_staff_and_menu_items():
    staff_list = report.get_staff_members()
    menu_list = report.get_menu_items()

    return jsonify(menu=menu_list, staff=staff_list)


@API_BLUEPRINT.route('/time/get_latest')
def get_latest_entry_time():
    time = report.get_latest_time()

    return jsonify(data=time)


@API_BLUEPRINT.route('/time/get_years')
def get_list_of_years():
    time = report.get_year_list()

    return jsonify(years=time)