"""
These tests check the constraints of the satisfaction relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from test.database.util import (
    insert_staff, insert_restaurant_table, insert_event,
    insert_customer_event, insert_reservation, insert_satisfaction
)


def test_empty_table(db_connection):
    """Check that the satisfaction table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM satisfaction")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid satisfaction record."""
    with db_connection.cursor() as curs:
        staff = insert_staff(curs, 'gcostanza', 'management')
        t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        e1 = insert_event(curs, 'seated', t1, staff)
        r1 = insert_reservation(curs, 1)
        insert_customer_event(curs, e1, r1)
        insert_satisfaction(curs, e1, r1, 100)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM satisfaction WHERE event_id = %s "
            "AND reservation_id = %s",
            (e1, r1)
        )
        assert curs.rowcount is 1


def test_no_customer_event(db_connection):
    """Assert that insertion fails when there is no customer event."""
    with db_connection.cursor() as curs:
        staff = insert_staff(curs, 'gcostanza', 'management')
        t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        e1 = insert_event(curs, 'seated', t1, staff)
        r1 = insert_reservation(curs, 1)

        with pytest.raises(psycopg2.IntegrityError):
            insert_satisfaction(curs, e1, r1, 100)


def test_invalid_score(db_connection):
    """Assert that insertion fails on an invalid score."""
    with db_connection.cursor() as curs:
        staff = insert_staff(curs, 'gcostanza', 'management')
        t1 = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
        e1 = insert_event(curs, 'seated', t1, staff)
        r1 = insert_reservation(curs, 1)

        with pytest.raises(psycopg2.IntegrityError):
            insert_satisfaction(curs, e1, r1, 101)
