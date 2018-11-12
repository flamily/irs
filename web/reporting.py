from web.db import db
from biz.css import manage_satisfaction as mcss
from biz import manage_staff as ms
from biz import manage_menu as mm
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

def format_menu_dict(menu_satisf):
    lst = []
    for item in menu_satisf:
        lst.append({
            "event_id":item[0],
            "description":float(item[1]),
            "date":item[2],
            "table_id":item[3],
            "staff_id":item[4],
            "reservation_id":item[5],
            "score":float(item[6])      #Format out Decimal type to prevent JSON errors
        })
    return lst

def sort_data(satisf_event):
    satisf_event.sort(key=lambda item:item['date'])
    return satisf_event

def get_staff_satisfaction_report(s_id, date_type, date_string):
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    return sort_data(format_dict(mcss.staff_css_between_dates(db, s_id, s_dt, e_dt)))

def get_menu_satisfaction(m_id, date_type, date_string):
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    item = mcss.get_menu_item_satisfaction(db, m_id, s_dt, e_dt)
    print(item)
    return sort_data(format_menu_dict(item))

def get_customer_satisfaciton(date_type, date_string):
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    return sort_data(format_dict(mcss.get_satisfaction_between_dates(db, s_dt, e_dt)))

def get_chart_data(response):
    labels = []
    data = []
    if response:
        labels=[x["date"] for x in response]
        data=[x["score"] for x in response]
        assert data[10] == response[10]["score"] and labels[10] == response[10]["date"]
    return labels, data

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

def get_staff_members():
    staff_list = ms.list_members(db)
    return [{"value": x.s_id, "name": "%s %s" % (x.first_name, x.last_name)} for x in staff_list]

def get_menu_items():
    menu_list = mm.list_menu(db)
    return [{"value": x.mi_id, "name": x.name} for x in menu_list]

def get_staff_average_score(s_id, date_type, date_string):
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    return float(mcss.avg_staff_css_between_dates(db, s_id, s_dt, e_dt))

def get_average_score(bounds, date):
    st, end = get_date_bounds(bounds, date)
    return float(mcss.avg_css_per_period(db, st, end))

def get_latest_time():
    date = mcss.get_latest_satisfaction_date(db)
    return date.strftime("%Y-%m-%d")

def get_year_list():
    return mcss.get_all_years(db)

def get_avg_menu_score(id, date_type, date_string):
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    return float(mcss.avg_menu_item_score(db, id, s_dt, e_dt))
