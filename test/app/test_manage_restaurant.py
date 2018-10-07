"""
These tests check the restaurant table manage.

Author: Andrew Pope
Date: 06/10/2018
"""
import pytest
import irs.app.manage_restaurant as mg
from irs.app.restaurant_table import State, Event, Shape
from irs.test.database.util import (
    insert_staff, insert_restaurant_table, insert_event
)


def test_create_reservation(database_snapshot):
    """Check that the manager can successfully create a reservation."""
    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            id1 = insert_restaurant_table(curs, 3, 1, 1, 'ellipse')
            id2 = insert_restaurant_table(curs, 2, 3, 4, 'rectangle')
            sid = insert_staff(curs, 'gcostanza', 'management')
            insert_event(curs, 'ready', id1, sid)
            insert_event(curs, 'ready', id2, sid)
            conn.commit()

        with conn.cursor() as curs:
            (event_id, reservation_id) = mg.create_reservation(
                conn, id1, sid, 5
            )  # NB - Does not currently validate group_size


def test_get_table(db_connection):
    """Check that the manager returns the correct table."""
    with db_connection.cursor() as curs:
        id1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        sid = insert_staff(curs, 'gcostanza', 'management')
        insert_event(curs, 'ready', id1, sid)

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
        insert_event(curs, 'ready', id1, sid)
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
            insert_event(curs, 'ready', id1, s_id)
            insert_event(curs, 'ready', id2, s_id)
            insert_event(curs, 'ready', id3, s_id)
            conn.commit()
            insert_event(curs, 'seated', id1, s_id)
            insert_event(curs, 'seated', id2, s_id)
            conn.commit()
            insert_event(curs, 'paid', id1, s_id)
            insert_event(curs, 'attending', id2, s_id)
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
