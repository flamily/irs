"""
These tests check the satisfaction manager.

Author: Andrew Pope, Andy Go, Jacob Vorreiter
Date: 11/11/2018
"""
import datetime
import biz.css.manage_satisfaction as ms
import biz.manage_restaurant as mr
import test.helper as h


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


def test_get_satisfaction_between_dates(database_snapshot):
    """Get satisfaction records between time periods"""
    db_connection = database_snapshot.getconn()
    t, staff = h.spoof_tables(db_connection, 3)
    db_connection.commit()

    dt1 = datetime.datetime(2018, 1, 1)
    dt2 = datetime.datetime(2018, 1, 4)
    dt3 = datetime.datetime(2018, 1, 6)

    scores = [[40, 60, 80, 100], [40, 60, 80], [40, 60, 80]]

    h.spoof_satisfaction(db_connection, t, staff, [dt1, dt2, dt3], scores)

    assert not ms.get_satisfaction_between_dates(
        db_connection, dt1.date(), dt1.date())
    assert not ms.get_satisfaction_between_dates(
        db_connection, dt1.date(), dt2.date())
    assert not ms.get_satisfaction_between_dates(
        db_connection, dt1.date(), dt3.date())
    assert not ms.get_satisfaction_between_dates(
        db_connection, dt2.date(), dt3.date())


def test_staff_css_between_dates(database_snapshot):
    """Get staff satisfaction records between time periods"""
    db_connection = database_snapshot.getconn()
    t, staff = h.spoof_tables(db_connection, 3)
    db_connection.commit()

    dt1 = datetime.datetime(2018, 1, 1)
    dt2 = datetime.datetime(2018, 1, 4)
    dt3 = datetime.datetime(2018, 1, 6)

    scores = [[40, 60, 80], [40, 60, 80], [40, 60, 80]]

    h.spoof_satisfaction(db_connection, t, staff, [dt1, dt2, dt3], scores)

    assert not ms.staff_css_between_dates(
        db_connection, staff, dt1.date(), dt1.date())
    assert not ms.staff_css_between_dates(
        db_connection, staff, dt1.date(), dt2.date())
    assert not ms.staff_css_between_dates(
        db_connection, staff, dt1.date(), dt3.date())
    assert not ms.staff_css_between_dates(
        db_connection, staff, dt2.date(), dt3.date())
    assert not ms.staff_css_between_dates(
        db_connection, staff+1, dt2.date(), dt3.date())


def test_get_menu_item_satisfaction(database_snapshot):
    """Get menu satisfaction records between time periods"""
    db_connection = database_snapshot.getconn()
    t, staff = h.spoof_tables(db_connection, 3)
    db_connection.commit()

    mi = h.spoof_menu_items(db_connection, 3)
    menu_items = [(mi[0], 2), (mi[1], 3), (mi[2], 1)]

    dt1 = datetime.datetime(2018, 1, 1)
    dt2 = datetime.datetime(2018, 1, 4)
    dt3 = datetime.datetime(2018, 1, 6)

    scores = [[40, 60, 80], [40, 60, 80, 100], [50, 55, 60]]

    h.spoof_satisfaction(
        db_connection,
        t,
        staff,
        [dt1, dt2, dt3],
        scores,
        [(1, 1)])

    assert len(ms.get_menu_item_satisfaction(
        db_connection, 1, dt1.date(), dt1.date())) == 1
    assert len(ms.get_menu_item_satisfaction(
        db_connection, 1, dt1.date(), dt2.date())) == 2
    assert len(ms.get_menu_item_satisfaction(
        db_connection, 1, dt3.date(), dt3.date())) == 1
    assert len(ms.get_menu_item_satisfaction(
        db_connection, 1, dt3.date(), dt3.date())[0]) == 6
    assert not ms.get_menu_item_satisfaction(
        db_connection, menu_items[2][0], dt2.date(), dt3.date())


def test_get_latest_satisfaction_date(database_snapshot):
    """Get latest satisfaction date"""
    db_connection = database_snapshot.getconn()
    t, staff = h.spoof_tables(db_connection, 1)
    db_connection.commit()

    dt1 = datetime.datetime(2018, 1, 1)
    dt_now = datetime.datetime.now().strftime("%Y-%m-%d")
    ce1 = mr.create_reservation(db_connection, t[0], staff, 5)
    ms.create_satisfaction(db_connection, 40, ce1[0], ce1[1])
    ce2 = mr.order(db_connection, [], t[0], staff)
    ms.create_satisfaction(db_connection, 80, ce2[0], ce2[1])
    ce3 = mr.paid(db_connection, t[0], staff)
    ms.create_satisfaction(db_connection, 60, ce3[0], ce3[1])
    h.update_reservation_dt(db_connection, ce1[1], ce1[0], dt1)
    h.update_reservation_dt(db_connection, ce2[1], ce2[0], dt1)
    h.update_reservation_dt(db_connection, ce3[1], ce3[0], dt1)

    assert dt_now in ms.get_latest_satisfaction_date(
        db_connection).strftime("%Y-%m-%d")


def test_get_all_years(database_snapshot):
    """Get all years"""
    db_connection = database_snapshot.getconn()
    t, staff = h.spoof_tables(db_connection, 1)
    db_connection.commit()

    dt1 = datetime.datetime(2017, 1, 1)
    dt_now = datetime.datetime.now().strftime("%Y")
    ce1 = mr.create_reservation(db_connection, t[0], staff, 5)
    ms.create_satisfaction(db_connection, 40, ce1[0], ce1[1])
    ce2 = mr.order(db_connection, [], t[0], staff)
    ms.create_satisfaction(db_connection, 80, ce2[0], ce2[1])
    ce3 = mr.paid(db_connection, t[0], staff)
    ms.create_satisfaction(db_connection, 60, ce3[0], ce3[1])
    h.update_reservation_dt(db_connection, ce1[1], ce1[0], dt1)
    h.update_reservation_dt(db_connection, ce2[1], ce2[0], dt1)
    h.update_reservation_dt(db_connection, ce3[1], ce3[0], dt1)

    assert dt_now == str(int(ms.get_all_years(
        db_connection)[0][0]))
    assert len(ms.get_all_years(
        db_connection)) == 2
