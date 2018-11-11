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
    return dict(page_title='IRS - Admin Dashboard')


@INDEX_BLUEPRINT.route('/test_dashboard')
def test():
    return render_template("index.html")

@INDEX_BLUEPRINT.route('/api/reporting/<type>')
def get_report(type):
    date_string = request.args.get('dateString')
    my_function = {
        "date": report_date,
        "week": report_week,
        "month": report_month,
        "year": report_year
    }.get(type, None)

    res = my_function(date_string)
    return jsonify(res)
