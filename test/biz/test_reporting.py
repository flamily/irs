"""
Reporting Interface tests

Author: Jacob Vorreiter
Date: 13/11/2018
"""

from biz import reporting as report


def test_get_date_bounds():
    """Test formatting function"""

    date_str = "2018-11-08"
    week = "2018-W45"
    month = "2018-11"
    year = "2018"

    start_date, end_date = report.get_date_bounds("date", date_str)
    assert start_date == date_str and end_date == date_str + " 23:59:59.998"

    start_date, end_date = report.get_date_bounds("week", week)
    assert start_date == "2018-11-05" and end_date == "2018-11-11 23:59:59.998"

    start_date, end_date = report.get_date_bounds("month", month)
    assert start_date == "2018-11-01" and end_date == "2018-11-30 23:59:59.998"

    start_date, end_date = report.get_date_bounds("year", year)
    assert start_date == "2018-01-01" and end_date == "2019-01-01 00:00:00.002"


def test_get_customer_satisfaction_missing(database_snapshot):
    """Get data from an empty database"""
    db_conn = database_snapshot.getconn()

    date_str = "2018-11-08"
    date_format = "date"

    assert report.get_customer_satisfaciton(
        db_conn,
        date_format,
        date_str) == ([], 0)


def test_get_staff_satisfaction_report_missing(database_snapshot):
    """Get data from an empty database"""
    db_conn = database_snapshot.getconn()

    date_str = "2018-11-08"
    date_format = "date"
    staff_id = 1

    assert report.get_staff_satisfaction_report(
        db_conn,
        staff_id,
        date_format,
        date_str) == ([], 0)


def test_get_menu_satisfaction_missing(database_snapshot):
    """Get data from an empty database"""
    db_conn = database_snapshot.getconn()

    date_str = "2018-11-08"
    date_format = "date"
    menu_id = 1

    assert report.get_menu_satisfaction(
        db_conn,
        menu_id,
        date_format,
        date_str) == ([], 0)


def test_get_staff_members_missing(database_snapshot):
    """Get data from an empty database"""
    db_conn = database_snapshot.getconn()

    assert report.get_staff_members(db_conn) == []


def test_get_menu_members_missing(database_snapshot):
    """Get data from an empty database"""
    db_conn = database_snapshot.getconn()

    assert report.get_menu_items(db_conn) == []


def test_get_latest_time_missing(database_snapshot):
    """Try to get the latest time from an empty database"""
    db_conn = database_snapshot.getconn()

    assert report.get_latest_time(db_conn) == ""
