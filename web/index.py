from flask import Blueprint, render_template, request, jsonify
import json

from web.decorators import templated, login_required
from web.reporting import report_date, report_week, report_month, report_year


# Reference for blueprints here:
# http://flask.pocoo.org/docs/1.0/blueprints/
INDEX_BLUEPRINT = Blueprint('index', __name__, template_folder='templates')

@INDEX_BLUEPRINT.route('/')
@login_required()
@templated(template='index.html')
def index():
    return dict(page_title='IRS - Admin Dashboard', test_page_title='IRS - TEST TITLE')


@INDEX_BLUEPRINT.route('/test_dashboard')
def test():
    return render_template("index.html")

@INDEX_BLUEPRINT.route('/api/reporting/<type>')
def get_report(type):
    date_string = request.args.get('dateString')

    print("Inbound function call: %s with date string: %s" % (type, date_string))

    my_function = {
        "date": report_date,
        "week": report_week,
        "month": report_month,
        "year": report_year
    }.get(type, None)

    res = my_function(date_string)

    json_ready = {
        "labels": res[0],
        "data": res[1]
    }
    print(json_ready)
    print(jsonify(labels=res[0], data=res[1]))

    return jsonify(({'labels':res[0], 'data':res[1]}))
