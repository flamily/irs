from flask import Blueprint, render_template

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
    labels, data = report_year("2018")
    print("=====================================================\n\n")
    print(labels)
    print("\n\n=====================================================")
    print("=====================================================\n\n")
    print(data)
    print("\n\n=====================================================")
    return render_template("index.html", chart_label=labels, chart_data=data)
