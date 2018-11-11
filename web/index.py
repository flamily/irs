from flask import Blueprint, render_template, request, jsonify
import json

from web.decorators import templated, login_required
from web.reporting import *


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
INDEX_BLUEPRINT = Blueprint('index', __name__, template_folder='templates')

@INDEX_BLUEPRINT.route('/')
@login_required()
@templated(template='index.html')
def index():
    return dict(page_title='IRS - Admin Dashboard')


@INDEX_BLUEPRINT.route('/test_dashboard')
def test():
    return render_template("index.html")

@INDEX_BLUEPRINT.route('/api/reporting/Customer/<type>')
def get_customer_report(type):
    date_string = request.args.get('dateString')
    print("'%s'" % type)
    my_function = {
        "date": report_date,
        "week": report_week,
        "month": report_month,
        "year": report_year
    }.get(type, None)
    assert my_function is not None
    print("Inbound endpoint call: %s Request: %s" % (type, date_string))
    res = my_function(date_string)
    labels = []
    data = []
    avg = ""
    if res:
        labels=[x["date"] for x in res]
        data=[x["score"] for x in res]
        assert data[10] == res[10]["score"] and labels[10] == res[10]["date"]

        avg = get_average_score(type, date_string)

    return jsonify(data=res, labels=labels, scores=data, average=avg)

@INDEX_BLUEPRINT.route('/api/reporting/Staff/<id>/<date_type>')
def get_staff_report(id, date_type):
    date_string = request.args.get('dateString')
    print("Inbound endpoint call: %s Request date: %s staff_id: %s" % (date_type, date_string, id))

    res = get_staff_satisfaction_report(id, date_type, date_string)
    if res:
        labels=[x["date"] for x in res]
        data=[x["score"] for x in res]
        assert data[10] == res[10]["score"] and labels[10] == res[10]["date"]

    return jsonify(data=res, labels=labels, scores=data, average=get_staff_average_score(id, date_type, date_string))
