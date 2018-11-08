"""
Driver for managing Analytics Reports records in the database.

This file contains a series of function that manipulate and access records
in the database pertaining to the Analytics Reports.
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
