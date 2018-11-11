"""
These tests check the satisfaction manager.

Author: Andrew Pope, Andy Go
Date: 11/11/2018
"""
import datetime
import biz.css.manage_satisfaction as ms
import biz.manage_restaurant as mr
import biz.manage_staff as mgs
import biz.manage_menu as mm
from biz.staff import Permission
from biz.restaurant_table import (Coordinate, Shape)


def __spoof_tables(db_conn, n, username, first, last):
    """Load a series of restaurant tables and a staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: ([t1_id, t2_id ... tn_id], staff_id)
    """
    staff_id = mgs.create_staff_member(
        db_conn, username, 'prettygood', (first, last),
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


# Functions for spoofing time
def __update_event_dt(db_conn, eid, dt):
    """Spoof an event's datetime.

    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "UPDATE event "
            "SET event_dt = %s "
            "WHERE event_id = %s",
            (dt, eid)
        )
        db_conn.commit()


def __update_reservation_dt(db_conn, rid, eid, dt):
    """Spoof a reservation's datetime.

    :param rid: The id of the reservation record to spoof.
    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with db_conn.cursor() as curs:
        __update_event_dt(db_conn, eid, dt)
        curs.execute(
            "UPDATE reservation "
            "SET reservation_dt = %s "
            "WHERE reservation_id = %s",
            (dt, rid)
        )
        db_conn.commit()


def test_create_satisfaction(database_snapshot):
    """Attempt to create a satisfaction order."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1, 'ldavid', 'Lt', 'David')
        conn.commit()
        (e1, r1) = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 100, e1, r1)
        assert ms.lookup_satisfaction(conn, e1, r1) == 100


def test_lookup_missing_satisfaction(database_snapshot):
    """Attempt to lookup a missing satisfaction."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1, 'ldavid', 'Lt', 'David')
        conn.commit()
        (e1, r1) = mr.create_reservation(conn, t[0], staff, 5)
        assert ms.lookup_satisfaction(conn, e1, r1) is None


def test_create_multiple_satisfaction(database_snapshot):
    """Create a satisfaciton record for multiple customer events."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1, 'ldavid', 'Lt', 'David')
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


def test_avg_css_per_period(database_snapshot):
    """Retrieve average css on and between 2018-01-01 and 2018-12-31"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1, 'ldavid', 'Lt', 'David')
        conn.commit()

        dt1 = datetime.datetime(2018, 1, 1)
        dt2 = datetime.datetime(2018, 12, 31)

        assert ms.avg_css_per_period(
            conn, dt1.date(), dt2.date()) is None

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 40, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 80, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 60, ce3[0], ce3[1])
        __update_reservation_dt(conn, ce1[1], ce1[0], dt1)
        __update_reservation_dt(conn, ce2[1], ce2[0], dt1)
        __update_reservation_dt(conn, ce3[1], ce3[0], dt1)

        assert ms.avg_css_per_period(
            conn, dt1.date(), dt1.date()) == 60
        assert ms.avg_css_per_period(
            conn, dt1.date(), dt2.date()) == 60
        assert ms.avg_css_per_period(
            conn, dt2.date(), dt2.date()) is None


def test_avg_css_per_staff(database_snapshot):
    """Retrieve average css for staff"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1, 'ldavid', 'Lt', 'David')
        t2, staff2 = __spoof_tables(conn, 1, 'lsarge', 'Lt', 'Sarge')

        conn.commit()

        assert ms.avg_css_per_staff(conn, 12345) is None

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 50, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 50, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 20, ce3[0], ce3[1])
        ce4 = mr.create_reservation(conn, t2[0], staff2, 5)
        ms.create_satisfaction(conn, 80, ce4[0], ce4[1])
        ce5 = mr.order(conn, [], t[0], staff2)
        ms.create_satisfaction(conn, 85, ce5[0], ce5[1])
        ce6 = mr.paid(conn, t2[0], staff2)
        ms.create_satisfaction(conn, 75, ce6[0], ce6[1])

        assert ms.avg_css_per_staff(conn, staff) == 40
        assert ms.avg_css_per_staff(conn, staff2) == 80


def test_avg_css_all_staff(database_snapshot):
    """Retrieve average css for staff"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1, 'ldavid', 'Lt', 'David')
        conn.commit()

        assert ms.avg_css_all_staff(conn) is None

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 80, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 20, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 50, ce3[0], ce3[1])

        avg_css = ms.avg_css_all_staff(conn)
        assert avg_css[0] == (1, 50)


def test_avg_css_per_menu_item(database_snapshot):
    """Retrieve average css for staff menu item"""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1, 'ldavid', 'Lt', 'David')
        conn.commit()

        assert ms.avg_css_per_menu_item(conn, 1) is None

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
