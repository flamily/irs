"""
These tests check the constraints of the reservation relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import insert_reservation


def test_empty_table(db_connection):
    """Check that the reservation table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM reservation")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid record."""
    with db_connection.cursor() as curs:
        r_id = insert_reservation(curs, 1)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM reservation WHERE reservation_id=%s",
            (r_id,)
        )
        assert curs.rowcount is 1


def test_no_customer_event(database_snapshot):
    """Assert a commited reservation will fail without a customer event."""
    error_msg = 'a reservation needs at least one associated customer event'

    with database_snapshot.getconn() as conn:
        with conn.cursor() as curs:
            r_id = insert_reservation(curs, 1)
            with pytest.raises(psycopg2.InternalError) as excinfo:
                conn.commit()
            assert error_msg in str(excinfo.value)

        with conn.cursor() as curs:
            curs.execute(
                "SELECT * FROM reservation WHERE reservation_id=%s",
                (r_id,)
            )
            assert curs.rowcount is 0


def test_invalid_group_size(db_connection):
    """Attempt to specify a negative table capacity."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.IntegrityError):
            insert_reservation(curs, -1)
