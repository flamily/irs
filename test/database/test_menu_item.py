"""
These tests check the constraints of the menu_item relation.

Author: Andrew Pope
Date: 04/10/2018
"""
import pytest
import psycopg2
from irs.test.database.util import insert_menu_item


def test_empty_table(db_connection):
    """Check that the menu_item table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM menu_item")
        assert curs.rowcount == 0


def test_valid(db_connection):
    """Enter a valid menu item."""
    name = 'spicy linguine'
    with db_connection.cursor() as curs:
        mi_id = insert_menu_item(curs, name)

    with db_connection.cursor() as curs:
        curs.execute(
            "SELECT name FROM menu_item WHERE menu_item_id = %s AND name = %s",
            (mi_id, name)
        )
        assert curs.rowcount == 1


def test_duplicate_item(db_connection):
    """Attempt to create two menu items with same name."""
    with db_connection.cursor() as curs:
        name = 'spagett'
        insert_menu_item(curs, name)
        with pytest.raises(psycopg2.IntegrityError):
            insert_menu_item(curs, name)


def test_pricing(db_connection):
    """Store valid prices to the database."""
    prices = {6.90, 0.75, 7.534, 0.999, 2.348}
    with db_connection.cursor() as curs:
        for price in prices:
            name = 'foo ' + str(price)
            mi = insert_menu_item(curs, name, price)
            curs.execute(
                "SELECT price FROM menu_item WHERE menu_item_id = %s",
                (mi,)
            )
            stored_price = curs.fetchone()[0]
            assert float(stored_price) == round(price, 2)


def test_expensive_item(db_connection):
    """Insert a price that exceeds the storage capability."""
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.DataError) as excinfo:
            insert_menu_item(curs, 'expensive', 1.5e9)
        assert "numeric field overflow" in str(excinfo.value)
