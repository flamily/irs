"""
These tests check the menu manager.

Author: Andrew Pope
Date: 09/10/2018
"""
import biz.manage_menu as menu
from biz.manage_menu import MenuItem


def test_empty_table(db_connection):
    """Check that the menu_item table has no records."""
    with db_connection.cursor() as curs:
        curs.execute("SELECT * FROM menu_item")
        assert curs.rowcount is 0


def test_create_menu(database_snapshot):
    """Attempt to create a series of menu items."""
    expected = [
        MenuItem(mi_id=None, name='spring rolls', description='', price=2.50),
        MenuItem(mi_id=None, name='wheat cakes', description='', price=3.25),
        MenuItem(mi_id=None, name='spagetti', description='', price=4.00)
    ]

    with database_snapshot.getconn() as conn:
        for item in expected:
            menu.create_menu_item(
                conn, item.name, item.description, item.price
            )

        actual = menu.list_menu(conn)
        assert len(actual) == 3
        for i in range(0, 3):
            assert actual[i].name == expected[i].name
            assert actual[i].description == expected[i].description
            assert actual[i].price == expected[i].price
