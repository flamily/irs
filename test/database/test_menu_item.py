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
        assert curs.rowcount is 0


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
        assert curs.rowcount is 1


def test_duplicate_item(db_connection):
    """Attempt to create two menu items with same name."""
    with db_connection.cursor() as curs:
        name = 'spagett'
        insert_menu_item(curs, name)
        with pytest.raises(psycopg2.IntegrityError):
            insert_menu_item(curs, name)
