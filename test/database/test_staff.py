"""
These tests check the constraints of the staff relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import insert_staff


def test_valid(db_connection):
    """Enter a valid staff record."""
    with db_connection.cursor() as curs:
        s_id = insert_staff(curs, 'gcostanza', 'management')

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT username FROM staff WHERE staff_id = %s AND username = %s",
            (s_id, "gcostanza")
        )
        assert curs.rowcount is 1


def test_invalid_permission(db_connection):
    """Attempt to bestow an invalid permission."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.DataError):
            insert_staff(curs, 'newman', 'soup-nazi')


def test_duplicate_user(db_connection):
    """Attempt to create two staff records with same username."""
    with db_connection.cursor() as curs:
        insert_staff(curs, 'kramer', 'management')
        with pytest.raises(psycopg2.IntegrityError):
            insert_staff(curs, 'kramer', 'wait_staff')
