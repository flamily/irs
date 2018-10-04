"""
A collection of database utility functions for testing.

Author: Andrew Pope
Date: 04/10/2018
"""


def insert_staff(db_cursor, username, permission):
    """Insert a staff record to the database."""
    db_cursor.execute(
        "INSERT INTO staff "
        "(username, password, first_name, last_name, permission) "
        "VALUES (%s, %s, %s, %s, %s) "
        "RETURNING staff_id",
        (
            username,
            'password',
            'John',
            'Doe',
            permission
        )
    )


def insert_restaurant_table(db_cursor, cap, width, height, shape):
    """Insert a restaurant table to the database."""
    db_cursor.execute(
        "INSERT INTO restaurant_table "
        "(capacity, x_pos, y_pos, width, height, shape) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "RETURNING restaurant_table_id",
        (
            cap,
            0,
            1,
            width,
            height,
            shape
        )
    )


def insert_menu_item(db_cursor, name):
    """Insert a menu item."""
    db_cursor.execute(
        "INSERT INTO menu_item "
        "(name, description) "
        "VALUES (%s, %s) "
        "RETURNING menu_item_id",
        (
            name,
            'A really hot and spicy dish.'
        )
    )
