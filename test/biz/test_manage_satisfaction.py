"""
These tests check the satisfaction manager.

Author: Andrew Pope
Date: 06/11/2018

Modified: Andy Go
Date: 10/11/2018
"""
import datetime
import biz.css.manage_satisfaction as ms
import biz.manage_restaurant as mr
import biz.manage_staff as mgs
import biz.manage_menu as mm
from biz.staff import Permission
from biz.restaurant_table import (Coordinate, Shape)


def __spoof_tables(db_conn, n):
    """Load a series of restaurant tables and a staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: ([t1_id, t2_id ... tn_id], staff_id)
    """
    staff_id = mgs.create_staff_member(
        db_conn, 'ldavid', 'prettygood', ('Larry', 'David'),
        Permission.wait_staff
    )

    tables = []
    for _ in range(0, n):
        tables.append(
            mr.create_restaurant_table(
                db_conn, 2, Coordinate(x=0, y=3), 1,
                5, Shape.rectangle, staff_id
            )[0]
        )
    return (tables, staff_id)


def __spoof_menu_items(db_conn, n):
    """Load a series of menu_items.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: [mi1_id, mi2_id ... min_id]
    """
    items = []
    for i in range(0, n):
        items.append(
            mm.create_menu_item(
                db_conn, str(i), 'a description', i
            )
        )
    return items


def test_create_satisfaction(database_snapshot):
    """Attempt to create a satisfaction order."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()
        (e1, r1) = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 100, e1, r1)
        assert ms.lookup_satisfaction(conn, e1, r1) == 100


def test_lookup_missing_satisfaction(database_snapshot):
    """Attempt to lookup a missing satisfaction."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()
        (e1, r1) = mr.create_reservation(conn, t[0], staff, 5)
        assert ms.lookup_satisfaction(conn, e1, r1) is None


def test_create_multiple_satisfaction(database_snapshot):
    """Create a satisfaciton record for multiple customer events."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 99, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 52, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 50, ce3[0], ce3[1])

        with conn.cursor() as curs:
            curs.execute(
                "SELECT * FROM satisfaction"
            )
            assert curs.rowcount == 3


def test_css_historic_time(database_snapshot):
    """Retrieve average css for staff"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 50, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 60, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 70, ce3[0], ce3[1])

        datetime_start = datetime.datetime(2018, 1, 1)
        datetime_end = datetime.datetime(2018, 12, 31)

        scores = ms.css_historic_time(
            conn, datetime_start.date(), datetime_end.date())
        assert scores[0].score == 50
        assert scores[1].score == 60
        assert scores[2].score == 70


def test_avg_css_per_period(database_snapshot):
    """Retrieve average css from __ to __"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 40, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 80, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 60, ce3[0], ce3[1])

        datetime_start = datetime.datetime(2018, 1, 1)
        datetime_end = datetime.datetime(2018, 12, 31)

        assert ms.avg_css_per_period(
            conn, datetime_start.date(), datetime_end.date()) == 60


def test_avg_css_per_staff(database_snapshot):
    """Retrieve average css for staff"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 80, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 20, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 50, ce3[0], ce3[1])

        assert ms.avg_css_per_staff(conn, staff) == 50


def test_avg_css_per_menu_item(database_snapshot):
    """Retrieve average css for staff menu item"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        mi = __spoof_menu_items(conn, 2)
        expected = [(mi[0], 2), (mi[1], 3)]
        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        (_, _, _) = mr.order(conn, expected, t[0], staff)
        ms.create_satisfaction(conn, 70, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 100, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 100, ce3[0], ce3[1])

        assert ms.avg_css_per_menu_item(conn, 1) == 90
