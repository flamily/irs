"""
These tests check the restaurant table manager.

Author: Andrew Pope
Date: 08/10/2018
"""
import pytest
import psycopg2
import biz.manage_restaurant as mg
import biz.manage_staff as ms
import biz.manage_menu as mm
from biz.staff import Permission
from biz.restaurant_table import (
    State, Event, Shape, Coordinate, RestaurantTable
)
from test.database.util import (
    insert_staff, insert_restaurant_table, insert_event
)

# Private global for quick spoofing of table data
__spoof = RestaurantTable(
    rt_id=1,  # Ignored in most places
    capacity=2,
    coordinate=Coordinate(x=0, y=3),
    width=1,
    height=5,
    shape=Shape.rectangle,
    latest_event=Event.ready
)


def __spoof_tables(db_conn, n):
    """Load a series of restaurant tables and a staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: ([t1_id, t2_id ... tn_id], staff_id)
    """
    staff_id = ms.create_staff_member(
        db_conn, 'ldavid', 'prettygood', ('Larry', 'David'),
        Permission.wait_staff
    )

    tables = []
    for _ in range(0, n):
        tables.append(
            mg.create_restaurant_table(
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


def test_lookup_missing_order(database_snapshot):
    """Attempt to lookup a reservation that has no order."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()
        (_, r1) = mg.create_reservation(conn, t[0], staff, 5)
        assert mg.lookup_order(conn, r1) is None


def test_lookup_order(database_snapshot):
    """Lookup a reservation's order."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()
        (_, r1) = mg.create_reservation(conn, t[0], staff, 5)
        (_, _, o1) = mg.order(conn, [], t[0], staff)
        lookedup = mg.lookup_order(conn, r1)
        assert o1 == lookedup


def test_no_reservation_for_order(database_snapshot):
    """Attempt to order for a table with no reservation."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        msg = 'no active reservation exists for table id: {}'.format(t[0])
        with pytest.raises(LookupError) as excinfo:
            mg.order(conn, [], t[0], staff)
        assert msg in str(excinfo.value)


def test_new_order(database_snapshot):
    """Attempt to create a new order for a reservation."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        mi = __spoof_menu_items(conn, 2)
        expected = [(mi[0], 2), (mi[1], 3)]
        (_, _) = mg.create_reservation(conn, t[0], staff, 5)
        (_, _, o1) = mg.order(conn, expected, t[0], staff)

        with conn.cursor() as curs:
            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (o1,)
            )
            order_items = curs.fetchall()
        assert len(order_items) == 2
        assert order_items[0][0] == mi[0]
        assert order_items[1][0] == mi[1]


def test_append_to_order(database_snapshot):
    """Attempt to append menu items to existing order."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()

        mi = __spoof_menu_items(conn, 3)
        expected = [(mi[0], 2), (mi[1], 3)]

        (_, _) = mg.create_reservation(conn, t[0], staff, 5)
        (_, _, o1) = mg.order(conn, expected, t[0], staff)

        with conn.cursor() as curs:
            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (o1,)
            )
            order_items = curs.fetchall()
        assert len(order_items) == 2
        assert order_items[0][0] == mi[0]
        assert order_items[1][0] == mi[1]

        (_, _, o2) = mg.order(conn, [(mi[2], 1)], t[0], staff)
        assert o1 == o2

        with conn.cursor() as curs:
            curs.execute(
                "SELECT menu_item_id from order_item "
                "WHERE customer_order_id = %s",
                (o1,)
            )
            order_items = curs.fetchall()
        assert len(order_items) == 3
        assert order_items[0][0] == mi[0]
        assert order_items[1][0] == mi[1]
        assert order_items[2][0] == mi[2]


def test_cant_ready(database_snapshot):
    """Attempt to maintain a seated table."""
    msg = "a table can only become ready after being paid or maintained"
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()
        mg.create_reservation(conn, t[0], staff, 5)

        with pytest.raises(psycopg2.InternalError) as excinfo:
            mg.ready(conn, t[0], staff)
        assert msg in str(excinfo.value)


def test_ready(database_snapshot):
    """Attempt to mark a table as ready."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()
        # Pay for table 1
        mg.create_reservation(conn, t[0], staff, 5)
        conn.commit()
        mg.paid(conn, t[0], staff)
        conn.commit()
        # Mark table 2 for maintainence
        mg.maintain(conn, t[1], staff)
        conn.commit()
        # Mark both as being ready
        mg.ready(conn, t[0], staff)
        mg.ready(conn, t[1], staff)
        for rt in mg.overview(conn):
            assert rt.latest_event is Event.ready
            assert rt.state is State.available


def test_cant_maintain(database_snapshot):
    """Attempt to maintain a seated table."""
    msg = "a table can only be maintained if it was initially ready"
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()
        mg.create_reservation(conn, t[0], staff, 5)

        with pytest.raises(psycopg2.InternalError) as excinfo:
            mg.maintain(conn, t[0], staff)
        assert msg in str(excinfo.value)


def test_maintain(database_snapshot):
    """Attempt to maintain a ready table."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()
        mg.maintain(conn, t[0], staff)
        table = mg.get_table(conn, t[0])
        assert table.latest_event is Event.maintaining
        assert table.state is State.unavailable


def test_cant_pay(database_snapshot):
    """Attempt to pay for a table that doesn't have an active reservation."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()

        msg = 'no active reservation exists for table id: {}'.format(t[0])
        with pytest.raises(LookupError) as excinfo:
            mg.paid(conn, t[0], staff)
        assert msg in str(excinfo.value)


def test_paid(database_snapshot):
    """Confirm that a reservation can be paid for."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()
        (_, r1) = mg.create_reservation(conn, t[0], staff, 5)
        conn.commit()
        (_, r2) = mg.paid(conn, t[0], staff)
        conn.commit()
        table = mg.get_table(conn, t[0])
        assert table.latest_event is Event.paid
        assert table.state is State.unavailable
        assert r1 == r2


def test_lookup_reservation_multiple(database_snapshot):
    """Check that the correct reservation is returned from multiple."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()

        mg.create_reservation(conn, t[0], staff, 2)
        (_, r2) = mg.create_reservation(conn, t[1], staff, 1)
        conn.commit()
        mg.paid(conn, t[0], staff)
        conn.commit()
        mg.ready(conn, t[0], staff)
        conn.commit()

        (_, r3) = mg.create_reservation(conn, t[0], staff, 2)
        assert mg.lookup_reservation(conn, t[0]) == r3
        assert mg.lookup_reservation(conn, t[1]) == r2


def test_lookup_reservation_simple(database_snapshot):
    """Check that the correct reservation is returned."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()
        (_, r1) = mg.create_reservation(conn, t[0], staff, 2)
        assert mg.lookup_reservation(conn, t[0]) == r1


def test_already_reserved(database_snapshot):
    """Check the manager fails when reserving an already reserved table."""
    msg = "a customer cannot be seated at a table if it was not available"
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 1)
        conn.commit()
        mg.create_reservation(conn, t[0], staff, 5)

        with pytest.raises(psycopg2.InternalError) as excinfo:
            mg.create_reservation(conn, t[0], staff, 5)
        assert msg in str(excinfo.value)


def test_create_reservation(database_snapshot):
    """Check that the manager can resolve a table id to a reservation."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 2)
        conn.commit()
        (e1, r1) = mg.create_reservation(conn, t[0], staff, 5)
        rt = mg.get_table(conn, t[0])
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
        t1 = insert_restaurant_table(curs, 3, 4, 5, 'ellipse')
        staff = insert_staff(curs, 'gcostanza', 'management')
        insert_event(curs, str(Event.ready), t1, staff)

    table = mg.get_table(db_connection, 1)
    assert table.rt_id == 1
    assert table.width == 4
    assert table.height == 5
    assert table.capacity == 3
    assert table.shape is Shape.ellipse
    assert table.state is State.available
    assert table.latest_event is Event.ready


def test_get_missing_table(db_connection):
    """Manager attempts to get non-existant table."""
    assert mg.get_table(db_connection, 69) is None


def test_overview(database_snapshot):
    """Check that the manager returns the correct states and tables."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 3)
        conn.commit()
        mg.create_reservation(conn, t[0], staff, 5)
        mg.create_reservation(conn, t[1], staff, 5)
        conn.commit()
        mg.paid(conn, t[0], staff)
        mg.order(conn, [], t[1], staff)
        conn.commit()

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


def test_available_tables(database_snapshot):
    """Check that the manager returns available tables."""
    with database_snapshot.getconn() as conn:
        t, staff = __spoof_tables(conn, 3)
        conn.commit()
        mg.create_reservation(conn, t[0], staff, 4)
        conn.commit()
        mg.paid(conn, t[0], staff)
        conn.commit()

        rt_list = mg.get_available_tables(conn, 1)
        assert len(rt_list) == 2
        assert rt_list[1].latest_event is Event.ready
        assert rt_list[2].latest_event is Event.ready


def test_table_creation(database_snapshot):
    """Check that a resturant table can be created."""
    expected = RestaurantTable(
        rt_id=1,
        capacity=2,
        coordinate=Coordinate(x=0, y=3),
        width=1,
        height=5,
        shape=Shape.rectangle,
        latest_event=Event.ready
    )

    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            staff = insert_staff(curs, 'gcostanza', 'management')
            conn.commit()

        t1 = mg.create_restaurant_table(
            conn, expected.capacity, expected.coordinate, expected.width,
            expected.height, expected.shape, staff
        )[0]

        actual = mg.get_table(conn, t1)
        assert actual.rt_id == t1
        assert actual.width == expected.width
        assert actual.height == expected.height
        assert actual.capacity == expected.capacity
        assert actual.shape is expected.shape
        assert actual.state is expected.state
        assert actual.latest_event is expected.latest_event
