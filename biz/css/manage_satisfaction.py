"""
Driver for managing and retreiving satisfaction records from the database.

Author: Andrew Pope, Andy GO, Jacob Vorreiter
Date: 12/11/2018
"""


def get_satisfaction_between_dates(db_conn, start, end):
    """Gets the customers satisfaction between dates across all
    staff and menu items

    :param db_conn: A psycopg2 connection to the databaseself.
    :param start: The start date in string form (ie 2018-10-25)
    :param end: The end date in string form
    :return: An SQL List of Tuples of all items"""

    sql = "SELECT * FROM event AS e \
           JOIN satisfaction AS s ON e.event_id = s.event_id \
           WHERE event_dt BETWEEN %s AND %s ORDER BY e.event_dt ASC"
    with db_conn.cursor() as curs:
        params = (start, end)
        curs.execute(sql, params)
        events = curs.fetchall()
        return events


def staff_css_between_dates(db_conn, staff_id, s_dt, e_dt):
    """Get staff member's satisfaction score between dates

    :param db_conn: A psycopg2 connection to the database.
    :param staff_id: The ID of the staff member.
    :param s_dt: The start date in string form (ie 25-10-25)
    :param e_dt: The end date in string form
    :return: List of Tuples of all staff items
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT * FROM event AS e "
            "JOIN satisfaction AS s ON e.event_id = s.event_id "
            "WHERE staff_id= %s AND event_dt BETWEEN %s AND %s "
            "ORDER BY e.event_dt ASC",
            (staff_id, s_dt, e_dt)
        )
        return curs.fetchall()


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


def avg_css_per_period(db_conn, datetime_start, datetime_end):
    """Average CSS only for specified time period.

    :param db_conn: A psycopg2 connection to the database.
    :param datetime_start: The starting datetime.date for the time period.
    :param datetime_end: The ending datetime.date for the time period.
    :return: Average satisfaction score for the time period.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT AVG(s.score) "
            "FROM satisfaction s "
            "JOIN reservation r ON s.reservation_id = r.reservation_id "
            "WHERE r.reservation_dt BETWEEN %s AND %s",
            (datetime_start, datetime_end)
        )
        avg_score = curs.fetchone()[0]
    return avg_score


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
        avg_scores = []
        if curs.rowcount < 1:
            return None
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


def get_menu_item_satisfaction(db_conn, menu_item, start_date, end_date):
    """Gets all records or specified menu_item in a specified time range.

    :param db_conn: A psycopg2 connection to the database.
    :param menu_item: The ID of the menu item.
    :param start_date: The start date in string form (ie 25-10-25)
    :param end_date: The end date in string form
    :return: SQL list of tuples of relevant data for menu item reporting
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT e.event_id, quantity, order_dt, restaurant_table_id, "
            "staff_id, s.reservation_id, score "
            "FROM satisfaction s "
            "JOIN reservation r ON s.reservation_id = r.reservation_id "
            "JOIN customer_order c ON r.reservation_id = c.reservation_id "
            "JOIN order_item oi ON c.customer_order_id = oi.customer_order_id "
            "JOIN menu_item mi ON oi.menu_item_id = mi.menu_item_id "
            "JOIN event e ON e.event_id = s.event_id "
            "WHERE s.score IS NOT NULL AND oi.menu_item_id = %s "
            "AND order_dt BETWEEN %s AND %s "
            "ORDER BY order_dt ASC",
            (menu_item, start_date, end_date)
        )
        return curs.fetchall()


def avg_menu_item_score(db_conn, menu_item, start_date, end_date):
    """Average CSS for specified menu_item.

    :param db_conn: A psycopg2 connection to the database.
    :param menu_item: The ID of the menu item.
    :param start_date: The start date in string form (ie 25-10-25)
    :param end_date: The end date in string form
    :return: Average CSS for the menu item between dates.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT AVG(score) "
            "FROM satisfaction s "
            "JOIN reservation r ON s.reservation_id = r.reservation_id "
            "JOIN customer_order c ON r.reservation_id = c.reservation_id "
            "JOIN order_item oi ON c.customer_order_id = oi.customer_order_id "
            "JOIN menu_item mi ON oi.menu_item_id = mi.menu_item_id "
            "JOIN event e ON e.event_id = s.event_id "
            "WHERE s.score IS NOT NULL AND oi.menu_item_id = %s "
            "AND order_dt BETWEEN %s AND %s",
            (menu_item, start_date, end_date)
        )
        return curs.fetchone()[0]


def get_latest_satisfaction_date(db_conn):
    """Average CSS for specified menu_item.

    :param db_conn: A psycopg2 connection to the database.
    :return: Gets latest data entry for initialisation of populated data.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT event_dt FROM event ORDER BY event_dt DESC",
        )
        if curs.rowcount < 1:
            return ""
        return curs.fetchone()[0]


def get_all_years(db_conn):
    """Average CSS for specified menu_item.

    :param db_conn: A psycopg2 connection to the database.
    :return: List of years that the data spans across.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT DISTINCT EXTRACT(YEAR FROM event_dt) FROM event",
        )
        return curs.fetchall()
