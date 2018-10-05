"""
These tests check the constraints of the event relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import (
    insert_staff, insert_restaurant_table, insert_event,
    insert_customer_event, insert_reservation
)


def test_empty_table(db_connection):
    """Check that the customer_event table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM customer_event")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid customer_event record."""
    with db_connection.cursor() as curs:
        s_id = insert_staff(curs, 'gcostanza', 'management')
        rt_id = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        e_id = insert_event(curs, 'seated', rt_id, s_id)
        r_id = insert_reservation(curs, 1)
        insert_customer_event(curs, e_id, r_id)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM customer_event WHERE event_id = %s "
            "AND reservation_id = %s",
            (e_id, r_id)
        )
        assert curs.rowcount is 1


def test_invalid_types(db_connection):
    """Check for an invalid customer_event types."""
    invalid = ['ready', 'maintaining']
    msg = 'a customer event can only be of types: seated, attended or paid'
    with db_connection.cursor() as curs:
        for type in invalid:
            s_id = insert_staff(curs, 'gcostanza', 'management')
            rt_id = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            e_id = insert_event(curs, type, rt_id, s_id)
            r_id = insert_reservation(curs, 1)

            with pytest.raises(psycopg2.InternalError) as excinfo:
                insert_customer_event(curs, e_id, r_id)
            assert msg in str(excinfo.value)
            db_connection.rollback()
