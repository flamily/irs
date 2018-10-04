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
        "values (%s, %s, %s, %s, %s)",
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
        "values (%s, %s, %s, %s, %s, %s)",
        (
            cap,
            0,
            1,
            width,
            height,
            shape
        )
    )
