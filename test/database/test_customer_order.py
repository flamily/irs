"""
These tests check the constraints of the customer_order relation.

Author: Andrew Pope
Date: 04/10/2018
"""
# pylint:disable=invalid-name
from irs.test.database.util import (
    insert_reservation, insert_customer_order
)


def test_empty_table(db_connection):
    """Check that the customer_order table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM customer_order")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid customer_order record."""
    with db_connection.cursor() as curs:
        r_id = insert_reservation(curs, 1)
        co_id = insert_customer_order(curs, r_id)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM customer_order WHERE customer_order_id = %s",
            (co_id,)
        )
        assert curs.rowcount is 1
