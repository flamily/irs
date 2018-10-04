"""
These tests check the constraints of the event relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import (
    insert_staff, insert_restaurant_table, insert_event
)


def test_valid(db_connection):
    """Enter a valid event record."""
    with db_connection.cursor() as curs:
        s_id = insert_staff(curs, 'gcostanza', 'management')
        rt_id = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        e_id = insert_event(curs, 'ready', rt_id, s_id)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM event WHERE event_id = %s",
            (e_id,)
        )
        assert curs.rowcount is 1

# TODO:
# - Tests that check invalid event type
# - Validate state change
