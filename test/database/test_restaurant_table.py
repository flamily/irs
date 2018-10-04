"""
These tests check the constraints of the restaurant_table relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import (
    insert_staff, insert_restaurant_table
)


def test_empty_table(db_connection):
    """Check that the staff table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM restaurant_table")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid staff record."""
    with db_connection.cursor() as curs:
        insert_restaurant_table(curs, 1, 1, 1, 'ellipse')

    expected = {
        'gcostanza': True,
    }
    with db_connection.cursor() as curs:
        curs.execute("SELECT username FROM staff")
        for staff in curs:
            print(staff)
            assert expected.pop(staff[0])
    assert len(expected) is 0
