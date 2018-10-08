"""
These tests check the restaurant table manager.

Author: Andrew Pope
Date: 06/10/2018
"""
# pylint:disable=invalid-name
import pytest
import psycopg2
import irs.app.manage_restaurant as mg
from irs.app.restaurant_table import State, Event, Shape
from irs.test.database.util import (
    insert_staff, insert_restaurant_table, insert_event, insert_customer_event,
    insert_menu_item
)


def test_lookup_missing_order(database_snapshot):
    """Attempt to lookup a reservation that has no order."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            conn.commit()

        (_, r1) = mg.create_reservation(conn, t1, staff, 5)
        with pytest.raises(TypeError):
            mg.lookup_order(conn, r1)


def test_lookup_order(database_snapshot):
    """Lookup a reservation's order."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            conn.commit()

        (_, r1) = mg.create_reservation(conn, t1, staff, 5)
        (_, _, o1) = mg.order(conn, [], t1, staff)
        lookedup = mg.lookup_order(conn, r1)
        assert o1 == lookedup


def test_append_to_order(database_snapshot):
    """Attempt to append menu items to existing order."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            conn.commit()

        with conn.cursor() as curs:
            m1 = insert_menu_item(curs, 'fried rice')
            m2 = insert_menu_item(curs, 'spring rolls')
            menu_items = [(m1, 2), (m2, 3)]
            conn.commit()

        (_, _) = mg.create_reservation(conn, t1, staff, 5)
        (_, _, o1) = mg.order(conn, menu_items, t1, staff)

        with conn.cursor() as curs:
            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (o1,)
            )
            order_items = curs.fetchall()
            assert len(order_items) == 2
            assert order_items[0][0] == m1
            assert order_items[1][0] == m2


def test_new_order(database_snapshot):
    """Attempt to create a new order for a reservation."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            conn.commit()

        with conn.cursor() as curs:
            m1 = insert_menu_item(curs, 'fried rice')
            m2 = insert_menu_item(curs, 'spring rolls')
            m3 = insert_menu_item(curs, 'dim sims')
            menu_items = [(m1, 2), (m2, 3)]
            conn.commit()

        (_, _) = mg.create_reservation(conn, t1, staff, 5)
        (_, _, o1) = mg.order(conn, menu_items, t1, staff)

        with conn.cursor() as curs:
            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (o1,)
            )
            order_items = curs.fetchall()
            assert len(order_items) == 2
            assert order_items[0][0] == m1
            assert order_items[1][0] == m2

        (_, _, o2) = mg.order(conn, [(m3, 1)], t1, staff)
        assert o1 == o2

        with conn.cursor() as curs:
            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (o1,)
            )
            order_items = curs.fetchall()
            assert len(order_items) == 3
            assert order_items[0][0] == m1
            assert order_items[1][0] == m2
            assert order_items[2][0] == m3


def test_cant_ready(database_snapshot):
    """Attempt to maintain a seated table."""
    msg = "a table can only become ready after being paid or maintained"
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.seated), t1, staff)
            conn.commit()

        with pytest.raises(psycopg2.InternalError) as excinfo:
            mg.ready(conn, t1, staff)
        assert msg in str(excinfo.value)


def test_ready(database_snapshot):
    """Attempt to mark a table as ready."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            t2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.paid), t1, staff)
            insert_event(curs, str(Event.maintaining), t2, staff)
            conn.commit()

        mg.ready(conn, t1, staff)
        mg.ready(conn, t2, staff)
        for rt in mg.overview(conn):
            assert rt.latest_event is Event.ready
            assert rt.state is State.available


def test_cant_maintain(database_snapshot):
    """Attempt to maintain a seated table."""
    msg = "a table can only be maintained if it was initially ready"
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.seated), t1, staff)
            conn.commit()

        with pytest.raises(psycopg2.InternalError) as excinfo:
            mg.maintain(conn, t1, staff)
        assert msg in str(excinfo.value)


def test_maintain(database_snapshot):
    """Attempt to maintain a ready table."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            conn.commit()

        mg.maintain(conn, t1, staff)
        table = mg.get_table(conn, t1)
        assert table.latest_event is Event.maintaining
        assert table.state is State.unavailable


def test_cant_pay(database_snapshot):
    """Attempt to pay for a table that doesn't have an active reservation."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            t2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            insert_event(curs, str(Event.ready), t2, staff)
            conn.commit()

        with pytest.raises(TypeError):
            mg.paid(conn, t1, staff)  # Fails to lookup a reservation id


def test_paid(database_snapshot):
    """Confirm that a reservation can be paid for."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            t2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            insert_event(curs, str(Event.ready), t2, staff)
            conn.commit()

        (_, r1) = mg.create_reservation(conn, t1, staff, 5)
        (_, r2) = mg.paid(conn, t1, staff)
        table = mg.get_table(conn, t1)
        assert table.latest_event is Event.paid
        assert table.state is State.unavailable
        assert r1 == r2


def test_lookup_reservation_multiple(database_snapshot):
    """Check that the correct reservation is returned from multiple."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            t2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            insert_event(curs, str(Event.ready), t2, staff)
            conn.commit()

        (_, r1) = mg.create_reservation(conn, t1, staff, 2)
        (_, r2) = mg.create_reservation(conn, t2, staff, 1)

        with conn.cursor() as curs:
            # Say that they paid
            e1 = insert_event(curs, str(Event.paid), t1, staff)
            insert_customer_event(curs, e1, r1)
            conn.commit()

        with conn.cursor() as curs:
            insert_event(curs, str(Event.ready), t1, staff)
            conn.commit()

        (_, r3) = mg.create_reservation(conn, t1, staff, 2)
        assert mg.lookup_reservation(conn, t1) == r3
        assert mg.lookup_reservation(conn, t2) == r2


def test_lookup_reservation_simple(database_snapshot):
    """Check that the correct reservation is returned."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            t2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            insert_event(curs, str(Event.ready), t2, staff)
            conn.commit()

        (_, r1) = mg.create_reservation(conn, t1, staff, 2)
        assert mg.lookup_reservation(conn, t1) == r1


def test_already_reserved(database_snapshot):
    """Check the manager fails when reserving an already reserved table."""
    msg = "a customer cannot be seated at a table if it was not available"
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            conn.commit()

        mg.create_reservation(conn, t1, staff, 5)

        with pytest.raises(psycopg2.InternalError) as excinfo:
            mg.create_reservation(conn, t1, staff, 5)
        assert msg in str(excinfo.value)


def test_create_reservation(database_snapshot):
    """Check that the manager can resolve a table id to a reservation."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            t2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            insert_event(curs, str(Event.ready), t2, staff)
            conn.commit()

        (e1, r1) = mg.create_reservation(conn, t1, staff, 5)
        rt = mg.get_table(conn, t1)
        assert rt.latest_event is Event.seated
        assert rt.state is State.occupied

        with conn.cursor() as curs:
            curs.execute(
                "SELECT * FROM customer_event WHERE event_id = %s "
                "AND reservation_id = %s",
                (e1, r1)
            )
            assert curs.rowcount is 1


def test_get_table(db_connection):
    """Check that the manager returns the correct table."""
    with db_connection.cursor() as curs:
        t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        staff = insert_staff(curs, 'gcostanza', 'management')
        insert_event(curs, str(Event.ready), t1, staff)

    table = mg.get_table(db_connection, 1)
    assert table.rt_id == 1
    assert table.shape is Shape.ellipse
    assert table.state is State.available
    assert table.latest_event is Event.ready


def test_get_missing_table(db_connection):
    """Manager attempts to get non-existant table."""
    msg = "'NoneType' object is not subscriptable"
    with db_connection.cursor() as curs:
        t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        staff = insert_staff(curs, 'gcostanza', 'management')
        insert_event(curs, str(Event.ready), t1, staff)

    with pytest.raises(TypeError) as excinfo:
        mg.get_table(db_connection, 69)  # Table 69 does not exist!
    assert msg in str(excinfo.value)


def test_overview(database_snapshot):
    """Check that the manager returns the correct states and tables."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            t2 = insert_restaurant_table(curs, 2, 3, 4, 'ellipse')
            t3 = insert_restaurant_table(curs, 2, 1, 5, 'ellipse')
            staff = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), t1, staff)
            insert_event(curs, str(Event.ready), t2, staff)
            insert_event(curs, str(Event.ready), t3, staff)
            conn.commit()

        mg.create_reservation(conn, t1, staff, 5)
        mg.create_reservation(conn, t2, staff, 5)
        mg.paid(conn, t1, staff)
        mg.order(conn, [], t2, staff)

        rt_list = mg.overview(conn)
        assert len(rt_list) == 3
        assert rt_list[0].rt_id == 1
        assert rt_list[0].state is State.unavailable
        assert rt_list[0].latest_event is Event.paid

        assert rt_list[1].rt_id == 2
        assert rt_list[1].state is State.occupied
        assert rt_list[1].latest_event is Event.attending

        assert rt_list[2].rt_id == 3
        assert rt_list[2].state is State.available
        assert rt_list[2].latest_event is Event.ready


def test_overview_empty(db_connection):
    """Check that the manager returns nothing."""
    assert not mg.overview(db_connection)
