from datetime import date, timedelta
import calendar

def get_satisfaction_between_dates(db_conn, start, end):
    sql = 'SELECT * FROM event AS e JOIN satisfaction AS s ON e.event_id = s.event_id WHERE event_dt BETWEEN %s AND %s'
    with db_conn.cursor() as curs:
        params = (start, end)
        curs.execute(sql, params)
        events = curs.fetchall()
        return events

def get_satisfactions_by_date(db_conn, date):
    """Get all satisfaction events of a specific date

    :param db_conn: A psycopg2 connection to the database.
    :param date: The date in format YYYY-MM-DD
    :return: [timestamps, satisfaction_scores].
    """

    return get_satisfaction_between_dates(db_conn, date, date + " 23:59:59.998")


def get_satisfactions_by_week(db_conn, year, week):
    """Get all satisfaction events over an entire week

    :param db_conn: A psycopg2 connection to the database.
    :param year: The year requested
    :param week: The the week number requested (eg 45)
    :return: [timestamps, satisfaction_scores].
    """
    week = week.lower().replace("w", "")

    d = date(int(year), 1, 1)
    dlt = timedelta(days = (int(week)-1)*7)
    week_start_date = d + dlt
    week_end_date = week_start_date + timedelta(days = 6)

    start_date = week_start_date.strftime("%Y-%m-%d")
    end_date = week_end_date.strftime("%Y-%m-%d") + " 23:59:59.998"

    return get_satisfaction_between_dates(db_conn, start_date, end_date)


def get_satisfactions_by_month(db_conn, year, month):
    """Get all satisfaction events over an entire week

    :param db_conn: A psycopg2 connection to the database.
    :param year: The year requested
    :param month: The month string (either full or abrv [October, Oct])
    :return: [timestamps, satisfaction_scores].
    """

    start_date = "%s-%s-%s" % (year, month, calendar.monthrange(int(year), int(month))[0] + 1)
    end_date = "%s-%s-%s 23:59:59.998" % (year, month, calendar.monthrange(int(year), int(month))[1])

    return get_satisfaction_between_dates(db_conn, start_date, end_date)


def get_satisfactions_by_year(db_conn, year):
    """Get all satisfaction events over an entire week

    :param db_conn: A psycopg2 connection to the database.
    :param year: The year requested
    :return: [timestamps, satisfaction_scores].
    """

    start_date = "%s-1-1" % (year)
    end_date = "%s-1-1 0:0:0.002" % (str(int(year) + 1))

    return get_satisfaction_between_dates(db_conn, start_date, end_date)
