from web.db import db
from biz import manage_reporting as mr

__MAX_GRAPH_ENTRIES__ = 15


def average_out_entries(labels, data):
    tmp_labels = []
    tmp_data = []
    averaging = int(len(labels) / __MAX_GRAPH_ENTRIES__ - 1 )

    tmp_score = 0
    for i in range(len(labels)):
        if i % averaging == 0:
            tmp_data.append(tmp_score / averaging)
            tmp_labels.append(labels[i])
            tmp_score = 0

        tmp_score += data[i]

    return [tmp_labels, tmp_data]

def formatted_lists(labels, data):
    if len(labels) > __MAX_GRAPH_ENTRIES__:
        return average_out_entries(labels, data)

    return [labels, data]

def report_date(date_str):
    labels, data = mr.get_satisfactions_by_date(db, date_str)
    return formatted_lists(labels, data)


def report_week(week_str):
    year = week_str.split("-")[0]
    week = week_str.split("-")[1].replace("W","")

    labels, data = mr.get_satisfactions_by_week(db, year, week)
    return formatted_lists(labels, data)

def report_month(month_str):
    year = month_str.split("-")[0]
    month = month_str.split("-")[1]

    labels, data = mr.get_satisfactions_by_month(db, year, month)
    return formatted_lists(labels, data)

def report_year(year_str):
    labels, data = mr.get_satisfactions_by_year(db, year_str)
    return formatted_lists(labels, data)
