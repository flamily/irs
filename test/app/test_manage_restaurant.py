"""
These tests check the restaurant table manage.

Author: Andrew Pope
Date: 06/10/2018
"""
import irs.app.manage_restaurant as mg
from irs.app.restaurant_table import State, Event
from irs.test.database.util import (
    insert_staff, insert_restaurant_table, insert_event
)


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
