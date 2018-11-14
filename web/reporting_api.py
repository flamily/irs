"""
Exposes endpoints for satisfaction data collection from the database

Author: Jacob Vorreiter
Date: 13/11/2018
"""


from flask import Blueprint, request, jsonify

from biz import reporting as report
from biz.css import manage_satisfaction as mcss
from web.db import db


class InvalidUsage(Exception):
    """Class to throw a JSON message with status_code default 400"""
    def __init__(self, message, status_code=400, payload=None):
        """Initialisation / Calling function for raising the Exception
        :param message: The string message to return
        :param status_code: The HTML error code
        :param payload: Additional payload items to return"""
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert the Exception items into a JSON ready dict"""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


API_BLUEPRINT = Blueprint('api', __name__, template_folder='templates')


@API_BLUEPRINT.route('/reporting/Customer/<date_type>')
def get_customer_report(date_type):
    """Reads in time parameters and returns customer scores
        between those times
    :param date_type: The type of time format (date, week, month, year)
    :return: JSON formatted data, with entries at:
        data, labels, scores, average
    """
    date_string = request.args.get('dateString')

    if not date_string:
        raise InvalidUsage("No date string provided")

    if date_type not in ["date", "week", "month", "year"]:
        raise InvalidUsage("Invalid date format provided")

    res, avg = report.get_customer_satisfaciton(db, date_type, date_string)
    labels, data = report.get_chart_data(res)

    return jsonify(data=res, labels=labels, scores=data, average=avg)


@API_BLUEPRINT.route('/reporting/Staff/<staff_id>/<date_type>')
def get_staff_report(staff_id, date_type):
    """Reads in time parameters and returns staff scores
        between those times
    :param staff_id: The ID of the staff to lookup
    :param date_type: The type of time format (date, week, month, year)
    :return: JSON formatted data, with entries at:
        data, labels, scores, average
    """
    date_string = request.args.get('dateString')

    if not date_string:
        raise InvalidUsage("No date string provided")

    if date_type not in ["date", "week", "month", "year"]:
        raise InvalidUsage("Invalid date format provided")

    if not staff_id.isdigit():
        raise InvalidUsage("Invalid staff_id provided")

    res, avg = report.get_staff_satisfaction_report(
        db,
        staff_id,
        date_type,
        date_string)
    labels, data = report.get_chart_data(res)

    return jsonify(data=res, labels=labels, scores=data, average=avg)


@API_BLUEPRINT.route('/reporting/Menu/<menu_id>/<date_type>')
def get_menu_score(menu_id, date_type):
    """Reads in time parameters and returns menu scores
        between those times
    :param menu_id: The ID of the menu item to lookup
    :param date_type: The type of time format (date, week, month, year)
    :return: JSON formatted data, with entries at:
        data, labels, scores, average
    """
    date_string = request.args.get('dateString')

    if not date_string:
        raise InvalidUsage("No date string provided")

    if date_type not in ["date", "week", "month", "year"]:
        raise InvalidUsage("Invalid date format provided")

    if not menu_id.isdigit():
        raise InvalidUsage("Invalid menu_id provided")

    res, avg = report.get_menu_satisfaction(db, menu_id, date_type, date_string)
    labels, scores = report.get_chart_data(res)

    return jsonify(data=res, labels=labels, scores=scores, average=avg)


@API_BLUEPRINT.route('/reporting/Staff//<date_type>')
def staff_missing_error(date_type):
    """Handles a missing staff id route
    :param date_type: UNUSED, The date type (date, week, month, year)"""
    # pylint: disable=unused-argument
    raise InvalidUsage("Missing staff_id from request")


@API_BLUEPRINT.route('/reporting/Menu//<date_type>')
def menu_missing_error(date_type):
    """Handles missing menu id route
    :param date_type: UNUSED, The date type (date, week, month, year)"""
    # pylint: disable=unused-argument
    raise InvalidUsage("Missing menu_id from request")


@API_BLUEPRINT.route('/reporting/list_items')
def get_staff_and_menu_items():
    """Reads staff ids, staff names, menu ids, menu names from the db
        to populate the Staff ID and Menu ID selectors

    :return: JSON formatted list with items menu, staff"""
    staff_list = report.get_staff_members(db)
    menu_list = report.get_menu_items(db)

    return jsonify(menu=menu_list, staff=staff_list)


@API_BLUEPRINT.route('/time/get_latest')
def get_latest_entry_time():
    """Gets the most recent record from the db to be used for
        initialisation loading

    :return: JSON formatted list with items data"""
    time = report.get_latest_time(db)

    return jsonify(data=time)


@API_BLUEPRINT.route('/time/get_years')
def get_list_of_years():
    """Gets list of all years in the db to populate the year selector

    :return: JSON formatted list with items years"""
    time = mcss.get_all_years(db)

    return jsonify(years=time)
