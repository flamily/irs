"""
These tests check the satisfaction manager.

Author: Andrew Pope
Date: 06/11/2018
"""
import biz.css.manage_satisfaction as ms
import biz.manage_restaurant as mr
import biz.manage_staff as staff
from biz.staff import Permission
from biz.restaurant_table import (Coordinate, Shape)


def __spoof_tables(db_conn, n):
    """Load a series of restaurant tables and a staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: ([t1_id, t2_id ... tn_id], staff_id)
    """
    staff_id = staff.create_staff_member(
        db_conn, 'ldavid', 'prettygood', ('Larry', 'David'),
        Permission.wait_staff
    )

    tables = []
    for _ in range(0, n):
        tables.append(
            mr.create_restaurant_table(
                db_conn, 2, Coordinate(x=0, y=3), 1,
                5, Shape.rectangle, staff_id
            )
        )
    return (tables, staff_id)


def test_create_menu(database_snapshot):
    """Attempt to lookup a reservation that has no order."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()
        (e1, r1) = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 100, e1, r1)
        assert ms.lookup_satisfaction(conn, e1, r1) == 100
