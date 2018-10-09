"""
Driver for managing the menu records in the database.

This file contains a series of functions that manipulate and access records
in the datbase pertaining to management of the restaurant menu.

Author: Andrew Pope
Date: 06/10/2018
"""
import collections

MenuItem = collections.namedtuple('MenuItem', 'mi_id name description price')


def list(db_conn):
    """Get a list of all menu items in the database.

    :param db_conn: A psycopg2 connection to the database.
    :return: A list of MenuItems.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT * FROM menu_item"
        )
        menu_items = []
        for item in curs.fetchall():
            menu_items.append(
                MenuItem(
                    mi_id=item[0],
                    name=item[1],
                    description=item[2],
                    price=float(item[3])
                )
            )

    return menu_items


def create_menu_item(db_conn, name, description, price):
    """Insert a menu items into the database.

    :param db_conn: A psycopg2 connection to the database.
    :param name: The name of the menu item.
    :param description: A description of the menu item.
    :param price: The price of the menu item.
    :return: Id of the newly created menu item.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "INSERT INTO menu_item "
            "(name, description, price) "
            "VALUES (%s, %s, %s) "
            "RETURNING menu_item_id",
            (
                name, description, price
            )
        )
        mi_id = curs.fetchone()[0]
        db_conn.commit()
    return mi_id
