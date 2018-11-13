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


def avg_css_per_period(db_conn, datetime_start, datetime_end, stride):
    """Average CSS only for specified time period.

    :param db_conn: A psycopg2 connection to the database.
    :param datetime_start: The starting datetime for the time period.
    :param datetime_end: The ending datetime for the time period.
    :param stride: The sub time period to split the
        averages (hour, week, month).
    :return: Average CSS score for the time period.
    """
    with db_conn.cursor() as curs:
        dt_start = datetime_start.strftime('%Y-%m-%d %H:%M:%S')
        dt_end = datetime_end.strftime('%Y-%m-%d %H:%M:%S')
        curs.execute(
            "SELECT DATE_PART(%s, r.reservation_dt), AVG(s.score) "
            "FROM satisfaction s "
            "JOIN reservation r ON s.reservation_id = r.reservation_id "
            "WHERE DATE_PART(%s, r.reservation_dt) "
            "BETWEEN DATE_PART(%s, %s::timestamp) "
            "AND DATE_PART(%s, %s::timestamp) "
            "GROUP BY DATE_PART(%s, r.reservation_dt) "
            "ORDER BY DATE_PART(%s, r.reservation_dt) ASC",
            (stride, stride, stride, dt_start,
             stride, dt_end, stride, stride)
        )
        if curs.rowcount < 1:
            return None
        avg_scores = []
        for item in curs.fetchall():
            dt_score = (item[0], item[1])
            avg_scores.append(dt_score)
    return avg_scores


def avg_css_per_staff(db_conn, staff_id):
    """Average CSS only for specified staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param staff_id: The ID of the exisiting staff record in the database.
    :return: Average satisfaction score for the staff member.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT AVG(s.score) "
            "FROM satisfaction s "
            "JOIN event e ON s.event_id = e.event_id "
            "WHERE e.staff_id = %s",
            ([staff_id])
        )
        avg_score = curs.fetchone()[0]
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
        if curs.rowcount < 1:
            return None
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
            "SELECT AVG(s.score) "
            "FROM satisfaction s "
            "JOIN reservation r ON s.reservation_id = r.reservation_id "
            "JOIN customer_order c ON r.reservation_id = c.reservation_id "
            "JOIN order_item oi ON c.customer_order_id = oi.customer_order_id "
            "WHERE s.score IS NOT NULL AND menu_item_id = %s",
            ([menu_item])
        )
        avg_score = curs.fetchone()[0]
    return avg_score
