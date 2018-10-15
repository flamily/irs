"""
These tests check the constraints of the order_item relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from test.database.util import (
    insert_order_item, insert_reservation, insert_customer_order,
    insert_menu_item
)


def test_empty_table(db_connection):
    """Check that the order_item table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM order_item")
        assert curs.rowcount is 0


def test_valid(db_connection):
    """Enter a valid record."""
    with db_connection.cursor() as curs:
        r_id = insert_reservation(curs, 1)
        co_id = insert_customer_order(curs, r_id)
        mi_id = insert_menu_item(curs, 'cereal')
        insert_order_item(curs, co_id, mi_id, 1)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT * FROM order_item WHERE menu_item_id=%s "
            "AND customer_order_id = %s",
            (mi_id, co_id)
        )
        assert curs.rowcount is 1


def test_invalid_quantity(db_connection):
    """Attempt to specify a negative quantity."""
    with db_connection.cursor() as curs:
        r_id = insert_reservation(curs, 1)
        co_id = insert_customer_order(curs, r_id)
        mi_id = insert_menu_item(curs, 'cereal')
        with pytest.raises(psycopg2.IntegrityError):
            insert_order_item(curs, co_id, mi_id, -1)


def test_duplicate_items(db_connection):
    """Attempt to add duplicate menu items."""
    with db_connection.cursor() as curs:
        r_id = insert_reservation(curs, 1)
        co_id = insert_customer_order(curs, r_id)
        mi_id = insert_menu_item(curs, 'cereal')

        insert_order_item(curs, co_id, mi_id, 2)
        insert_order_item(curs, co_id, mi_id, 3)
