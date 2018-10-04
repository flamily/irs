"""
These tests check the simple and advanced constraints of the irs db schema.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2


# Group tests by files instead of by classes (i.e. create a database sub-folder)
# in the test folder.
#
# It's probably also a good idea to create a util class.


def insert_record(db_cursor, username, permission):
    """Insert a record to the database."""
    db_cursor.execute(
        "INSERT INTO staff "
        "(username, password, first_name, last_name, permission) "
        "values (%s, %s, %s, %s, %s)",
        (
            username,
            'password',
            'John',
            'Doe',
            permission
        )
    )

def test_empty_table(db_connection):
    """Check that the staff table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT username FROM staff")
        assert curs.rowcount is 0

def test_valid(db_connection):
    """Enter a valid staff record."""
    with db_connection.cursor() as curs:
        insert_record(curs, 'gcostanza', 'management')

    expected = {
        'gcostanza': True,
    }
    with db_connection.cursor() as curs:
        curs.execute("SELECT username FROM staff")
        for staff in curs:
            print(staff)
            assert expected.pop(staff[0])
    assert len(expected) is 0


def test_non_existant_table(db_connection):
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.ProgrammingError):
            curs.execute("SELECT username FROM wew_lad")
