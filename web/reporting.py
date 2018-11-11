from web.db import db
from biz import manage_reporting as mr
import datetime
from decimal import Decimal

__MAX_GRAPH_ENTRIES__ = 15


def average_out_entries(labels, data):
    tmp_labels = []
    tmp_data = []
    averaging = int(len(labels) / __MAX_GRAPH_ENTRIES__ - 1 )

    tmp_score = 0
    for i in range(len(labels)):
        if i % averaging == 0:
            tmp_data.append(float(float(tmp_score) / float(averaging)))
            tmp_labels.append(labels[i])
            tmp_score = 0

        tmp_score += data[i]

    return [tmp_labels, tmp_data]

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
    print(lst)
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
