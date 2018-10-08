"""
These tests check the restaurant table manager.

Author: Andrew Pope
Date: 06/10/2018
"""
import pytest
import psycopg2
import irs.app.manage_restaurant as mg
from irs.app.restaurant_table import State, Event, Shape
from irs.test.database.util import (
    insert_staff, insert_restaurant_table, insert_event, insert_customer_event,
    insert_menu_item
)

def test_lookup_missing_order(db_connection):
    assert True

def test_lookup_order(db_connection):
    assert True


def test_append_to_order(database_snapshot):
    """Attempt to append menu items to existing order."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            conn.commit()

        with conn.cursor() as curs:
            m1 = insert_menu_item(curs, 'fried rice')
            m2 = insert_menu_item(curs, 'spring rolls')

            menu_items = [(m1, 2), (m2, 3)]
            conn.commit()

        with conn.cursor() as curs:
            (_, rid) = mg.create_reservation(conn, id1, sid, 5)
            (_, r2id, oid) = mg.order(conn, menu_items, id1, sid)

            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (oid,)
            )
            order_items = curs.fetchall()
            assert len(order_items) == 2
            assert order_items[0][0] == m1
            assert order_items[1][0] == m2


def test_new_order(database_snapshot):
    """Attempt to create a new order for a reservation."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            conn.commit()

        with conn.cursor() as curs:
            m1 = insert_menu_item(curs, 'fried rice')
            m2 = insert_menu_item(curs, 'spring rolls')
            m3 = insert_menu_item(curs, 'dim sims')
            menu_items = [(m1, 2), (m2, 3)]
            conn.commit()

        with conn.cursor() as curs:
            (_, _) = mg.create_reservation(conn, id1, sid, 5)
            (_, _, oid) = mg.order(conn, menu_items, id1, sid)

            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (oid,)
            )
            order_items = curs.fetchall()
            assert len(order_items) == 2
            assert order_items[0][0] == m1
            assert order_items[1][0] == m2

            (_, _, o2id) = mg.order(conn, [(m3, 1)], id1, sid)
            assert oid == o2id
            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (oid,)
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
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.seated), id1, sid)
            conn.commit()

        with conn.cursor() as curs:
            with pytest.raises(psycopg2.InternalError) as excinfo:
                mg.ready(conn, id1, sid)
            assert msg in str(excinfo.value)


def test_ready(database_snapshot):
    """Attempt to mark a table as ready."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.paid), id1, sid)
            insert_event(curs, str(Event.maintaining), id2, sid)
            conn.commit()

        with conn.cursor() as curs:
            mg.ready(conn, id1, sid)
            mg.ready(conn, id2, sid)
            for rt in mg.overview(conn):
                assert rt.latest_event is Event.ready
                assert rt.state is State.available


def test_cant_maintain(database_snapshot):
    """Attempt to maintain a seated table."""
    msg = "a table can only be maintained if it was initially ready"
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.seated), id1, sid)
            conn.commit()

        with conn.cursor() as curs:
            with pytest.raises(psycopg2.InternalError) as excinfo:
                mg.maintain(conn, id1, sid)
            assert msg in str(excinfo.value)


def test_maintain(database_snapshot):
    """Attempt to maintain a ready table."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            conn.commit()

        with conn.cursor() as curs:
            mg.maintain(conn, id1, sid)
            rt = mg.get_table(conn, id1)
            assert rt.latest_event is Event.maintaining
            assert rt.state is State.unavailable


def test_cant_pay(database_snapshot):
    """Attempt to pay for a table that doesn't have an active reservation."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            insert_event(curs, str(Event.ready), id2, sid)
            conn.commit()

        with conn.cursor() as curs:
            with pytest.raises(TypeError):
                mg.paid(conn, id1, sid)  # Fails to lookup a reservation id


def test_paid(database_snapshot):
    """Confirm that a reservation can be paid for."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            insert_event(curs, str(Event.ready), id2, sid)
            conn.commit()

        with conn.cursor() as curs:
            (eid, rid) = mg.create_reservation(conn, id1, sid, 5)
            (_, r2id) = mg.paid(conn, id1, sid)
            rt = mg.get_table(conn, id1)
            assert rt.latest_event is Event.paid
            assert rt.state is State.unavailable
            assert rid == r2id


def test_lookup_reservation_multiple(database_snapshot):
    """Check that the correct reservation is returned from multiple."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            insert_event(curs, str(Event.ready), id2, sid)
            conn.commit()

        with conn.cursor() as curs:
            (_, r1id) = mg.create_reservation(conn, id1, sid, 2)
            (_, r2id) = mg.create_reservation(conn, id2, sid, 1)
            # Say that they paid
            e1 = insert_event(curs, str(Event.paid), id1, sid)
            conn.commit()
            insert_customer_event(curs, e1, r1id)
            insert_event(curs, str(Event.ready), id1, sid)
            conn.commit()
            (_, r3id) = mg.create_reservation(conn, id1, sid, 2)

        with conn.cursor() as curs:
            assert mg.lookup_reservation(conn, id1) == r3id
            assert mg.lookup_reservation(conn, id2) == r2id


def test_lookup_reservation_simple(database_snapshot):
    """Check that the correct reservation is returned."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            insert_event(curs, str(Event.ready), id2, sid)
            conn.commit()

        with conn.cursor() as curs:
            (_, rid) = mg.create_reservation(conn, id1, sid, 2)

        with conn.cursor() as curs:
            assert mg.lookup_reservation(conn, id1) == rid


def test_already_reserved(database_snapshot):
    """Check the manager fails when reserving an already reserved table."""
    msg = "a customer cannot be seated at a table if it was not available"
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            conn.commit()

        with conn.cursor() as curs:
            (_, rid) = mg.create_reservation(conn, id1, sid, 5)

        with pytest.raises(psycopg2.InternalError) as excinfo:
            mg.create_reservation(conn, id1, sid, 5)
        assert msg in str(excinfo.value)


def test_create_reservation(database_snapshot):
    """Check that the manager can resolve a table id to a reservation."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, sid)
            insert_event(curs, str(Event.ready), id2, sid)
            conn.commit()

        with conn.cursor() as curs:
            # NB - Does not currently validate group_size
            (eid, rid) = mg.create_reservation(conn, id1, sid, 5)
            rt = mg.get_table(conn, id1)
            assert rt.latest_event is Event.seated
            assert rt.state is State.occupied

        with conn.cursor() as curs:
            curs.execute(
                "SELECT * FROM customer_event WHERE event_id = %s "
                "AND reservation_id = %s",
                (eid, rid)
            )
            assert curs.rowcount is 1


def test_get_table(db_connection):
    """Check that the manager returns the correct table."""
    with db_connection.cursor() as curs:
        id1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        sid = insert_staff(curs, 'gcostanza', 'management')
        insert_event(curs, str(Event.ready), id1, sid)

        rt = mg.get_table(db_connection, 1)
        assert rt.rt_id == 1
        assert rt.shape is Shape.ellipse
        assert rt.state is State.available
        assert rt.latest_event is Event.ready


def test_get_missing_table(db_connection):
    """Manager attempts to get non-existant table."""
    msg = "'NoneType' object is not subscriptable"
    with db_connection.cursor() as curs:
        id1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        sid = insert_staff(curs, 'gcostanza', 'management')
        insert_event(curs, str(Event.ready), id1, sid)
        with pytest.raises(TypeError) as excinfo:
            mg.get_table(db_connection, 69)
        assert msg in str(excinfo.value)


def test_overview(database_snapshot):
    """Check that the manager returns the correct states and tables."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'ellipse')
            id3 = insert_restaurant_table(curs, 2, 1, 5, 'ellipse')
            s_id = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, str(Event.ready), id1, s_id)
            insert_event(curs, str(Event.ready), id2, s_id)
            insert_event(curs, str(Event.ready), id3, s_id)
            conn.commit()
            insert_event(curs, str(Event.seated), id1, s_id)
            insert_event(curs, str(Event.seated), id2, s_id)
            conn.commit()
            insert_event(curs, str(Event.paid), id1, s_id)
            insert_event(curs, str(Event.attending), id2, s_id)
            conn.commit()

        with conn.cursor() as curs:
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
    assert len(mg.overview(db_connection)) == 0
