"""
Interface to customer satisfaction and dashboard relevant endpoint queries,
includes helper functions

Author: Jacob Vorreiter
Date: 12/11/2018
"""

from biz.css import manage_satisfaction as mcss
from biz import manage_staff as ms
from biz import manage_menu as mm
from datetime import date, timedelta
import calendar


def do_avg(item):
    avg = 0
    for i in item:
        avg += (i[-1]/len(item))
    return float(avg)


def format_dict(satisf_event):
    """Formats the inbound satisfaction event SQL tuple into a JSON ready list

    :param satisf_event: The raw output from the SQL query
    :return: A list of dict objects, removing unwanted Decimal() types and
    converting to float
    :note: This function is used to sort satisfaction and staff sql tuples only
    """
    lst = []
    for item in satisf_event:
        lst.append({
            "date": item[0],
            "reservation_id": item[1],
            "table_id": item[2],
            "staff": item[3],
            "menu": item[4],
            "score": float(item[5])  # Remove Decimal() prevent JSON errors
            })
    return lst


def sort_data(satisf_event):
    """Sorts data based on date, in ascending order

    :param satisf_event: The formatted, JSON ready list of dicts
    :return: Sorted version of satisf_event
    """

    satisf_event.sort(key=lambda item: item['date'])
    return satisf_event


def get_chart_data(response):
    """Obtains dates and scores to be used in the chart for labels and data
    entries

    :param response: The sorted, formatted, JSON ready list of dicts
    :return: Tuple containing labels first, then data
    """
    labels = []
    data = []
    if response:
        labels = [x["date"] for x in response]
        data = [x["score"] for x in response]
    return labels, data


def get_date_bounds(bounds, date_str):
    """Gets start and end date strings to prepare for Sql query

    :param bounds: The string representation of which type of function to
    execute (date, week, month, year)
    :param date_str: The string supplied from the request
    (YYYY-MM-DD, YYYY-WeekNumber [eg W45], YYYY-MM, YYYY)
    :return: Start and end dates in the string form YYYY-MM-DD
    """
    date_str = date_str.lower().replace("w", "")
    start_date = ""
    end_date = ""
    if bounds == "date":
        start_date = date_str
        end_date = date_str + " 23:59:59.998"
    elif bounds == "week":
        year, week = date_str.split('-')
        d = date(int(year), 1, 1)
        dlt = timedelta(days=(int(week)-1)*7)
        week_start_date = d + dlt
        week_end_date = week_start_date + timedelta(days=6)
        start_date = week_start_date.strftime("%Y-%m-%d")
        end_date = week_end_date.strftime("%Y-%m-%d") + " 23:59:59.998"

    elif bounds == "month":
        year, month = date_str.split("-")
        start_date = "%s-%s-%s" % (year, month, "01")
        end_date = "%s-%s-%s 23:59:59.998" % (year, month, calendar.monthrange(
            int(year), int(month))[1])

    elif bounds == "year":
        start_date = "%s-01-01" % (date_str)
        end_date = "%s-01-01 00:00:00.002" % (str(int(date_str) + 1))

    return start_date, end_date


def get_customer_satisfaciton(db, date_type, date_string):
    """Gets, formats and sorts customer satisfaction from the SQL library

    :param db: the database connection
    :param date_type: String representation of date function
    (date, week, month, year)
    :param date_string: The string supplied from the request
    (YYYY-MM-DD, YYYY-WeekNumber [eg W45], YYYY-MM, YYYY)
    :return: JSON ready list of dicts containing satisfaction reporting data
    """
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    item = mcss.get_satisfaction_between_dates(db, s_dt, e_dt)

    if item:
        return (sort_data(format_dict(item)), do_avg(item))
    return ([], 0)


def get_staff_satisfaction_report(db, s_id, date_type, date_string):
    """Gets, formats and sorts staff satisfaction from the SQL library

    :param db: the database connection
    :param: s_id: Staff ID to send to SQL query
    :param date_type: String representation of date function
    (date, week, month, year)
    :param date_string: The string supplied from the request
    (YYYY-MM-DD, YYYY-WeekNumber [eg W45], YYYY-MM, YYYY)
    :return: JSON ready list of dicts containing staff satisfaction
    reporting data
    """
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    item = mcss.staff_css_between_dates(db, s_id, s_dt, e_dt)

    if item:
        return (sort_data(format_dict(item)), do_avg(item))
    return ([], 0)


def get_menu_satisfaction(db, m_id, date_type, date_string):
    """Gets, formats and sorts menu satisfaction from the SQL library

    :param db: the database connection
    :param m_id: The Menu ID to send to SQL query
    :param date_type: String representation of date function
    (date, week, month, year)
    :param date_string: The string supplied from the request
    (YYYY-MM-DD, YYYY-WeekNumber [eg W45], YYYY-MM, YYYY)
    :return: JSON ready list of dicts containing menu satisfaction
    reporting data
    """
    s_dt, e_dt = get_date_bounds(date_type, date_string)
    item = mcss.get_menu_item_satisfaction(db, m_id, s_dt, e_dt)

    if item:
        return (sort_data(format_dict(item)), do_avg(item))
    return ([], 0)


def get_staff_members(db):
    """Gets a list of staff ids and names to populate front end selector

    :param db: the database connection
    :return: list of dictionary items with value, name: staff_id, full_name
    """
    staff_list = ms.list_members(db)

    if staff_list:
        return [{"value": x.s_id, "name": "%s %s" %
                                          (x.first_name, x.last_name)}
                for x in staff_list]
    return []


def get_menu_items(db):
    """Gets a list of menu ids and names to populate front end selector

    :param db: the database connection
    :return: list of dictionary items with value, name: menu_id, menu_name
    """
    menu_list = mm.list_menu(db)
    if menu_list:
        return [{"value": x.mi_id, "name": x.name} for x in menu_list]
    return []


def get_latest_time(db):
    """Gets the datetime of the latest entry in the database

    :param db: the database connection
    :return: date picker reader formatted datestring
    :note: this is required to correctly load in initialisation data on
    document load
    """
    latest_date = mcss.get_latest_satisfaction_date(db)

    if latest_date:
        return latest_date.strftime("%Y-%m-%d")
    return ""
