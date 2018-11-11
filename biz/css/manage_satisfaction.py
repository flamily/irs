"""
Driver for managing and retreiving satisfaction records from the database.

Author: Andrew Pope, Andy GO
Date: 11/11/2018
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


# pylint:disable=too-few-public-methods,too-many-arguments
class CSS():
    """Object version of CSS data from satisfaction and event table"""

    def __init__(self, ev_id, rv_id, score, description, ev_dt, rt_id, st_id):
        self.ev_id = int(ev_id)
        self.rv_id = int(rv_id)
        self.score = int(score)
        self.st_id = int(st_id)
        self.description = str(description)
        self.ev_dt = ev_dt
        self.rt_id = int(rt_id)


def css_historic_time(db_conn, datetime_start, datetime_end):
    """Historic CSS and related data for specified time period.

    :param db_conn: A psycopg2 connection to the database.
    :param datetime_start: The starting datetime.date for the time period.
    :param datetime_end: The ending datetime.date for the time period.
    :return: Object containing columns from satisfaction and events table.
    """
    with db_conn.cursor() as curs:
        curs.execute("SELECT s.event_id, s.reservation_id, s.score, staff_id, "
                     "e.description, e.event_dt, e.restaurant_table_id "
                     "FROM satisfaction s "
                     "JOIN event e ON e.event_id = s.event_id "
                     "WHERE e.event_dt BETWEEN %s AND %s "
                     "ORDER BY e.event_dt ASC",
                     (datetime_start, datetime_end)
                     )
        css = []
        for row in curs.fetchall():
            css.append(CSS(
                ev_id=row[0],
                rv_id=row[1],
                score=row[2],
                st_id=row[3],
                description=row[4],
                ev_dt=row[5],
                rt_id=row[6],))
    return css


def avg_css_per_period(db_conn, datetime_start, datetime_end):
    """Average CSS only for specified time period.

    :param db_conn: A psycopg2 connection to the database.
    :param datetime_start: The starting datetime.date for the time period.
    :param datetime_end: The ending datetime.date for the time period.
    :return: Average satisfaction score for the time period.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT s.score "
            "FROM satisfaction s "
            "JOIN reservation r ON s.reservation_id = r.reservation_id "
            "WHERE r.reservation_dt BETWEEN %s AND %s",
            (datetime_start, datetime_end)
        )
        scores = []
        for score in curs.fetchall():
            scores.extend(score)
        avg_score = sum(scores) / len(scores)
    return avg_score


def avg_css_per_staff(db_conn, staff_id):
    """Average CSS only for specified staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param staff_id: The ID of the exisiting staff record in the database.
    :return: Average satisfaction score for the staff member.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT s.score "
            "FROM satisfaction s "
            "JOIN event e ON s.event_id = e.event_id "
            "WHERE e.staff_id = %s",
            ([staff_id])
        )
        scores = []
        for score in curs.fetchall():
            scores.extend(score)
        avg_score = sum(scores) / len(scores)
    return avg_score


def avg_css_all_staff(db_conn):
    """Average CSS for all staff members.

    :param db_conn: A psycopg2 connection to the database.
    :return: Tuple containing the staff ID and their corresponding average CSS.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT e.staff_id, AVG(s.score) "
            "FROM satisfaction s "
            "JOIN event e ON s.event_id = e.event_id "
            "GROUP BY e.staff_id ORDER BY e.staff_id ASC"
        )
        avg_scores = []
        for item in curs.fetchall():
            staff_score = (item[0], item[1])
            avg_scores.append(staff_score)
    return avg_scores


def avg_css_per_menu_item(db_conn, menu_item):
    """Average CSS for specified menu_item.

    :param db_conn: A psycopg2 connection to the database.
    :param menu_item: The ID of the menu item.
    :return: Average CSS for the menu item.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT score "
            "FROM satisfaction s "
            "JOIN reservation r ON s.reservation_id = r.reservation_id "
            "JOIN customer_order c ON r.reservation_id = c.reservation_id "
            "JOIN order_item oi ON c.customer_order_id = oi.customer_order_id "
            "WHERE s.score IS NOT NULL AND menu_item_id = %s",
            ([menu_item])
        )
        scores = []
        for score in curs.fetchall():
            scores.extend(score)
        avg_score = sum(scores) / len(scores)
    return avg_score
