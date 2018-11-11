from web.db import db
from biz import manage_reporting as mr
from biz.css import manage_satisfaction as mcss
from datetime import date, datetime, timedelta, timezone
import calendar

def get_timestamp(date):
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    timestamp = (date - epoch) / timedelta(seconds=1)
    return {
        "display": date,
        "timestamp": timestamp
    }

def format_dict(satisf_event):
    lst = []
    for item in satisf_event:
        lst.append({
            "event_id":item[0],
            "description":item[1],
            "date":item[2],
            "table_id":item[3],
            "staff_id":item[4],
            "reservation_id":item[6],   #We skip item[5] here because item[5] is just event_id again
            "score":float(item[7])      #Format out Decimal type to prevent JSON errors
        })
    return lst

def sort_data(satisf_event):
    satisf_event.sort(key=lambda item:item['date'])
    return satisf_event

def report_date(date_str):
    satisf_event = mr.get_satisfactions_by_date(db, date_str)
    return sort_data(format_dict(satisf_event))


def report_week(week_str):
    year = week_str.split("-")[0]
    week = week_str.split("-")[1].replace("W","")

    satisf_event = mr.get_satisfactions_by_week(db, year, week)
    return sort_data(format_dict(satisf_event))

def report_month(month_str):
    year = month_str.split("-")[0]
    month = month_str.split("-")[1]

    satisf_event = mr.get_satisfactions_by_month(db, year, month)
    return sort_data(format_dict(satisf_event))

def report_year(year_str):
    satisf_event = mr.get_satisfactions_by_year(db, year_str)
    return sort_data(format_dict(satisf_event))

def get_staff_satisfaction_report(s_id, date_type, date_string):
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    return sort_data(format_dict(mcss.staff_css_between_dates(db, s_id, s_dt, e_dt)))

def get_date_bounds(bounds, date_str):
    date_str = date_str.lower().replace("w", "")
    start_date = ""
    end_date = ""
    if bounds == "date":
        start_date = date_str
        end_date = date_str + " 23:59:59.998"
    elif bounds == "week":
        year, week = date_str.split('-')
        d = date(int(year), 1, 1)
        dlt = timedelta(days = (int(week)-1)*7)
        week_start_date = d + dlt
        week_end_date = week_start_date + timedelta(days = 6)
        start_date = week_start_date.strftime("%Y-%m-%d")
        end_date = week_end_date.strftime("%Y-%m-%d") + " 23:59:59.998"

    elif bounds == "month":
        year, month = date_str.split("-")
        start_date = "%s-%s-%s" % (year, month, calendar.monthrange(int(year), int(month))[0] + 1)
        end_date = "%s-%s-%s 23:59:59.998" % (year, month, calendar.monthrange(int(year), int(month))[1])

    elif bounds == "year":
        start_date = "%s-1-1" % (date_str)
        end_date = "%s-1-1 0:0:0.002" % (str(int(date_str) + 1))

    return start_date, end_date

def get_staff_average_score(s_id, date_type, date_string):
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    return float(mcss.avg_staff_css_between_dates(db, s_id, s_dt, e_dt))

def get_average_score(bounds, date):
    st, end = get_date_bounds(bounds, date)
    return float(mcss.avg_css_per_period(db, st, end))
