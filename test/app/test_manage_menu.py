"""
These tests check the menu manager.

Author: Andrew Pope
Date: 09/10/2018
"""
import pytest
import psycopg2
import irs.app.manage_menu as menu
from irs.app.manage_menu import MenuItem


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

        list = menu.list(conn)
        assert len(list) == 3
        for i in range(0, 3):
            assert list[i].name == expected[i].name
            assert list[i].description == expected[i].description
            assert list[i].price == expected[i].price
