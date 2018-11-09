"""
Driver for managing and retreiving satisfaction records from the database.

Author: Andrew Pope
Date: 06/11/2018
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


"""
    * CSS values across time (daily, weekly, monthly) entry vs exit
    * Dropdown for specific timing per filter
    * Average CSS for specified time period
    * Average CSS per staff member
    * Graph historic CSS values for staff member and show on graph.
    * Trend of selected meals from group (nice to have)
"""


def retrieve_avg_score(db_conn):
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT *"
            "FROM satisfaction s"
            "JOIN reservation r on r.reservation_id = s.reservation_id"
            "LIMIT 10"
        )
        if curs.rowcount != 1:
            return None
        avg_score = curs.fetchone()[0]
    return avg_score
