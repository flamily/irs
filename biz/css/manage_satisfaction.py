"""
Driver for managing and retreiving satisfaction records from the database.

Author: Andrew Pope, Andy GO, Jacob Vorreiter
Date: 12/11/2018
"""

CUSTOMER_SQL = """
    select
        1,
        array_to_string(array_agg(distinct m.name), ', '),
        r_date,
        restaurant_table_id,
        array_to_string(array_agg(distinct s.first_name), ', '),
        reservation_id,
        delta
    from css_reporting cr
    join menu_item as m on m.menu_item_id = cr.menu_item_id
    join staff as s on s.staff_id = cr.staff_id
    where r_date BETWEEN %s AND %s
    group by r_date, restaurant_table_id, reservation_id, delta
    order by r_date ASC;
    """

STAFF_SQL = """
    select distinct
        1,
        'a',
        r_date,
        restaurant_table_id,
        staff_id,
        reservation_id,
        delta
    from css_reporting as cr
    where staff_id= %s AND r_date BETWEEN %s AND %s
    order by r_date ASC
    """

MENU_SQL = """
    select distinct
        1,
        'a',
        r_date,
        restaurant_table_id,
        array_agg(distinct staff_id),
        reservation_id,
        delta
    from css_reporting as cr
    where menu_item_id= %s AND r_date BETWEEN %s AND %s
    group by r_date, restaurant_table_id, reservation_id, delta
    order by r_date ASC
    """


def get_satisfaction_between_dates(db_conn, start, end):
    """Gets the customers satisfaction between dates across all
    staff and menu items

    :param db_conn: A psycopg2 connection to the databaseself.
    :param start: The start date in string form (ie 2018-10-25)
    :param end: The end date in string form
    :return: An SQL List of Tuples of all items"""

    with db_conn.cursor() as curs:
        params = (start, end)
        curs.execute(CUSTOMER_SQL, params)
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
            STAFF_SQL,
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
            MENU_SQL,
            (menu_item, start_date, end_date)
        )
        return curs.fetchall()


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
