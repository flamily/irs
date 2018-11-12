"""
These tests check the satisfaction manager.

Author: Andrew Pope, Andy Go
Date: 11/11/2018
"""
import datetime
import biz.css.manage_satisfaction as ms
import biz.manage_restaurant as mr
import test.helper as h
import biz.manage_menu as mm


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
        t, staff = h.spoof_tables(conn, 1)
        conn.commit()
        (e1, r1) = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 100, e1, r1)
        assert ms.lookup_satisfaction(conn, e1, r1) == 100


def test_lookup_missing_satisfaction(database_snapshot):
    """Attempt to lookup a missing satisfaction."""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)
        conn.commit()
        (e1, r1) = mr.create_reservation(conn, t[0], staff, 5)
        assert ms.lookup_satisfaction(conn, e1, r1) is None


def test_create_multiple_satisfaction(database_snapshot):
    """Create a satisfaciton record for multiple customer events."""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)
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
        t, staff = h.spoof_tables(conn, 1)
        conn.commit()

        dt1 = datetime.datetime(2018, 1, 1)
        dt2 = datetime.datetime(2018, 12, 31)
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


def test_missing_avg_css_per_period(database_snapshot):
    """Retrieve missing average css on 2018-12-31"""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)
        conn.commit()

        dt1 = datetime.datetime(2018, 1, 1)
        dt2 = datetime.datetime(2018, 12, 31)

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        __update_reservation_dt(conn, ce1[1], ce1[0], dt1)

        assert ms.avg_css_per_period(
            conn, dt2.date(), dt2.date()) is None


def test_avg_css_per_staff(database_snapshot):
    """Retrieve average css for specified staff"""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)
        t2, staff2 = h.spoof_tables(conn, 1, 'lsarge', 'Lt', 'Sarge')

        conn.commit()

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


def test_missing_avg_css_per_staff(database_snapshot):
    """Retrieve missing average css for specified staff"""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)

        conn.commit()

        mr.create_reservation(conn, t[0], staff, 5)
        assert ms.avg_css_per_staff(conn, 12345) is None


def test_avg_css_all_staff(database_snapshot):
    """Retrieve average css for all staff"""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)
        t2, staff2 = h.spoof_tables(conn, 1, 'lsarge', 'Lt', 'Sarge')

        conn.commit()

        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 10, ce1[0], ce1[1])
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 20, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 30, ce3[0], ce3[1])
        ce4 = mr.create_reservation(conn, t2[0], staff2, 5)
        ms.create_satisfaction(conn, 40, ce4[0], ce4[1])
        ce5 = mr.order(conn, [], t[0], staff2)
        ms.create_satisfaction(conn, 50, ce5[0], ce5[1])
        ce6 = mr.paid(conn, t2[0], staff2)
        ms.create_satisfaction(conn, 60, ce6[0], ce6[1])

        avg_css = ms.avg_css_all_staff(conn)
        assert avg_css[0] == (staff, 20)
        assert avg_css[1] == (staff2, 50)


def test_missing_avg_css_all_staff(database_snapshot):
    """Retrieve missing average css for all staff"""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)

        conn.commit()

        mr.create_reservation(conn, t[0], staff, 5)

        assert ms.avg_css_all_staff(conn) is None


def test_avg_css_per_menu_item(database_snapshot):
    """Retrieve average css for specified menu item"""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)
        conn.commit()

        assert ms.avg_css_per_menu_item(conn, 1) is None

        mi = __spoof_menu_items(conn, 2)
        expected = [(mi[0], 2), (mi[1], 3)]
        ce1 = mr.create_reservation(conn, t[0], staff, 5)
        ms.create_satisfaction(conn, 70, ce1[0], ce1[1])
        (_, _, _) = mr.order(conn, expected, t[0], staff)
        ce2 = mr.order(conn, [], t[0], staff)
        ms.create_satisfaction(conn, 100, ce2[0], ce2[1])
        ce3 = mr.paid(conn, t[0], staff)
        ms.create_satisfaction(conn, 100, ce3[0], ce3[1])

        assert ms.avg_css_per_menu_item(conn, 1) == 90


def test_missing_avg_css_per_menu_item(database_snapshot):
    """Retrieve missing average css for specified menu item"""
    with database_snapshot.getconn() as conn:
        t, staff = h.spoof_tables(conn, 1)
        conn.commit()

        mr.create_reservation(conn, t[0], staff, 5)

        assert ms.avg_css_per_menu_item(conn, 1) is None
