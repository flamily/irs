"""
These tests check the constraints of the restaurant_table relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import insert_restaurant_table


def test_empty_table(db_connection):
    """Check that the restaurant_table table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM restaurant_table")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid record."""
    with db_connection.cursor() as curs:
        rt_id = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM restaurant_table WHERE restaurant_table_id=%s",
            (rt_id,)
        )
        assert curs.rowcount is 1


def test_no_event(database_snapshot):
    """Assert that a commited resturant table will error without an event."""
    expected_error = 'a restaurant table needs at least one associated event'

    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            rt_id = insert_restaurant_table(curs, 1, 1, 1, 'ellipse')
            with pytest.raises(psycopg2.InternalError) as excinfo:
                conn.commit()
            assert expected_error in str(excinfo.value)

        with conn.cursor() as curs:
            curs.execute(
                "SELECT * FROM restaurant_table WHERE restaurant_table_id=%s",
                (rt_id,)
            )
            assert curs.rowcount is 0


def test_invalid_capacity(db_connection):
    """Attempt to specify a negative table capacity."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.IntegrityError):
            insert_restaurant_table(curs, -2, 1, 1, 'ellipse')


def test_invalid_width(db_connection):
    """Attempt to specify negative width."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.IntegrityError):
            insert_restaurant_table(curs, 2, -5, 1, 'ellipse')


def test_invalid_height(db_connection):
    """Attempt to specify negative height."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.IntegrityError):
            insert_restaurant_table(curs, 2, 5, -1, 'ellipse')


def test_invalid_shape(db_connection):
    """Attempt to specify an invalid shape."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.DataError):
            insert_restaurant_table(curs, 2, 5, 1, 'not-a-shape')
