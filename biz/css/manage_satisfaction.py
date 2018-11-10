"""
Driver for managing and retreiving satisfaction records from the database.

Author: Andrew Pope
Date: 06/11/2018

Modified: Andy Go
Date: 10/11/2018
"""


def create_satisfaction(db_conn, score, event_id, reservation_id):
    """Store a calculated satisfaction score in the database.

    :param db_conn: A psycopg2 connection to the database.
    :param score: The customer satisfaction score to store.
    :param event_id: The ID of an existing event record in the database.
    :param reservation_id: The ID of an existing reservation in the database.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "INSERT INTO satisfaction "
            "(event_id, reservation_id, score) "
            "VALUES (%s, %s, %s) ",
            (
                event_id, reservation_id, score
            )
        )


def lookup_satisfaction(db_conn, event_id, reservation_id):
    """Get satisfaction for a customer event if it exists.

    :param db_conn: A psycopg2 connection to the database.
    :param event_id: The ID of an existing event record in the database.
    :param reservation_id: The ID of an existing reservation in the database.
    :return: Satisfaction score or None if record does not exist.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT score FROM satisfaction "
            "WHERE event_id = %s AND reservation_id = %s",
            (event_id, reservation_id)
        )
        if curs.rowcount != 1:
            return None
        score = curs.fetchone()[0]
    return score

    # * CSS values across time (daily, weekly, monthly) entry vs exit
    # * Dropdown for specific timing per filter
    # * Graph historic CSS values for staff member and show on graph.
    # * Trend of selected meals from group (nice to have)


# pylint:disable=too-few-public-methods,too-many-arguments
class CSS():
    """Object version of CSS data from satisfaction and event table"""

    def __init__(self, ev_id, rv_id, score, description, ev_dt, rt_id, st_id):
        self.ev_id = int(ev_id)
        self.rv_id = int(rv_id)
        self.score = int(score)
        self.description = str(description)
        self.ev_dt = ev_dt
        self.rt_id = int(rt_id)
        self.st_id = int(st_id)


def css_historic_time(db_conn, datetime_start, datetime_end):
    """Average CSS for specified time period

    :param db_conn: A psycopg2 connection to the database.
    :param datetime_start: The starting datetime.date for the time period.
    :param datetime_end: The ending datetime.date for the time period.
    """
    with db_conn.cursor() as curs:
        curs.execute("SELECT s.event_id, s.reservation_id, score,"
                     "description, event_dt, restaurant_table_id, staff_id "
                     "FROM satisfaction s "
                     "JOIN event e ON e.event_id = s.event_id "
                     "WHERE e.event_dt BETWEEN %s AND %s",
                     (datetime_start, datetime_end)
                     )
        scores = []
        for score in curs.fetchall():
            scores.append(CSS(
                ev_id=score[0],
                rv_id=score[1],
                score=score[2],
                description=score[3],
                ev_dt=score[4],
                rt_id=score[5],
                st_id=score[6]))
    return scores


def css_per_period(db_conn, datetime_start, datetime_end):
    """Average CSS for specified time period

    :param db_conn: A psycopg2 connection to the database.
    :param datetime_start: The starting datetime.date for the time period.
    :param datetime_end: The ending datetime.date for the time period.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT AVG(score) "
            "FROM satisfaction s "
            "INNER JOIN ("
            " SELECT *"
            " FROM reservation r"
            " JOIN customer_event ce ON ce.reservation_id = r.reservation_id"
            " WHERE r.reservation_dt BETWEEN %s AND %s) sub "
            "ON s.event_id = sub.event_id",
            (datetime_start, datetime_end)
        )
        if curs.rowcount != 1:
            return None
        avg_score = int(curs.fetchone()[0])
    return avg_score


def css_per_staff(db_conn, staff_id):
    """Average CSS for specified staff member

    :param db_conn: A psycopg2 connection to the database.
    :param staff_id: The ID of the exisiting staff record in the database.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT AVG(score) "
            "FROM satisfaction s "
            "INNER JOIN ("
            " SELECT *"
            " FROM event e"
            " JOIN customer_event ce ON ce.event_id = e.event_id"
            " WHERE e.staff_id = %s) sub "
            "ON s.reservation_id = sub.reservation_id",
            ([staff_id])
        )
        if curs.rowcount != 1:
            return None
        avg_score = int(curs.fetchone()[0])
    return avg_score
