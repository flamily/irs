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


def test_empty_table(db_connection):
    """Check that the event table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM event")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid event record."""
    with db_connection.cursor() as curs:
        staff = insert_staff(curs, 'gcostanza', 'management')
        t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        e1 = insert_event(curs, 'ready', t1, staff)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM event WHERE event_id = %s",
            (e1,)
        )
        assert curs.rowcount is 1


def test_invalid_type(db_connection):
    """Check for an invalid event type."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.DataError):
            staff = insert_staff(curs, 'gcostanza', 'management')
            t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            insert_event(curs, 'fake', t1, staff)


def assert_valid_change(db_connection, start_e, end_e, table_id, staff):
    """Assert that a change between a start and end event is valid."""
    print('valid event change: {} -> {}'.format(start_e, end_e))
    with db_connection.cursor() as curs:
        e1 = insert_event(curs, start_e, table_id, staff)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM event WHERE event_id = %s",
            (e1,)
        )
        assert curs.rowcount is 1

    with db_connection.cursor() as curs:
        e1 = insert_event(curs, end_e, table_id, staff)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM event WHERE event_id = %s",
            (e1,)
        )
        assert curs.rowcount is 1


def test_valid_changes(db_connection):
    """Check all the valid state changes available through the event table."""
    valid_changes = [
        ('ready', 'seated'),
        ('ready', 'maintaining'),
        ('maintaining', 'ready'),
        ('seated', 'attending'),
        ('seated', 'paid'),
        ('attending', 'attending'),
        ('attending', 'paid'),
        ('paid', 'ready')
    ]
    with db_connection.cursor() as curs:
        for start_e, end_e in valid_changes:
            staff = insert_staff(curs, 'gcostanza', 'management')
            t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            assert_valid_change(db_connection, start_e, end_e, t1, staff)
            db_connection.rollback()


def assert_invalid_change(db_connection, start_e, end_e, table_id, staff, msg):
    """Assert that a change between a start and end event is invalid."""
    # pylint: disable=R0913
    print('invalid event change: {} -> {}'.format(start_e, end_e))
    with db_connection.cursor() as curs:
        e1 = insert_event(curs, start_e, table_id, staff)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM event WHERE event_id = %s",
            (e1,)
        )
        assert curs.rowcount is 1

    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.InternalError) as excinfo:
            e1 = insert_event(curs, end_e, table_id, staff)
        assert msg in str(excinfo.value)


def test_invalid_change(db_connection):
    """Check all the invalid state changes through the event table."""
    msg1 = 'a table can only become ready after being paid or maintained'
    msg2 = 'a table can only be maintained if it was initially ready'
    msg3 = 'a customer cannot be seated at a table if it was not available'
    msg4 = 'a table cannot be attended if not currently occupied by customers'
    msg5 = 'only an occupied table can be paid for'

    invalid_changes = [
        ('seated', 'ready', msg1),
        ('attending', 'ready', msg1),
        ('ready', 'ready', msg1),
        ('seated', 'maintaining', msg2),
        ('attending', 'maintaining', msg2),
        ('paid', 'maintaining', msg2),
        ('maintaining', 'maintaining', msg2),
        ('paid', 'seated', msg3),
        ('maintaining', 'seated', msg3),
        ('attending', 'seated', msg3),
        ('seated', 'seated', msg3),
        ('ready', 'attending', msg4),
        ('paid', 'attending', msg4),
        ('maintaining', 'attending', msg4),
        ('ready', 'paid', msg5),
        ('maintaining', 'paid', msg5),
        ('paid', 'paid', msg5),
    ]

    with db_connection.cursor() as curs:
        for start_e, end_e, msg in invalid_changes:
            staff = insert_staff(curs, 'gcostanza', 'management')
            t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            assert_invalid_change(
                db_connection, start_e, end_e, t1, staff, msg
            )
            db_connection.rollback()
