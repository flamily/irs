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
            username, 'password', 'John', 'Doe', permission
        )
    )

    return db_cursor.fetchone()[0]


def insert_restaurant_table(db_cursor, cap, width, height, shape):
    """Insert a restaurant table to the database."""
    db_cursor.execute(
        "INSERT INTO restaurant_table "
        "(capacity, x_pos, y_pos, width, height, shape) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "RETURNING restaurant_table_id",
        (
            cap, 0, 1, width, height, shape
        )
    )

    return db_cursor.fetchone()[0]


def insert_menu_item(db_cursor, name):
    """Insert a menu item."""
    db_cursor.execute(
        "INSERT INTO menu_item "
        "(name, description) "
        "VALUES (%s, %s) "
        "RETURNING menu_item_id",
        (
            name, 'A really hot and spicy dish.'
        )
    )

    return db_cursor.fetchone()[0]


def insert_event(db_cursor, description, restaurant_table_id, staff_id):
    """Insert a menu item."""
    db_cursor.execute(
        "INSERT INTO event "
        "(description, restaurant_table_id, staff_id) "
        "VALUES (%s, %s, %s) "
        "RETURNING event_id",
        (
            description, restaurant_table_id, staff_id
        )
    )

    return db_cursor.fetchone()[0]


def insert_reservation(db_cursor, group_size):
    """Insert a reservation."""
    db_cursor.execute(
        "INSERT INTO reservation "
        "(group_size) "
        "VALUES (%s) "
        "RETURNING reservation_id",
        (
            group_size,
        )
    )

    return db_cursor.fetchone()[0]


def insert_customer_event(db_cursor, e_id, r_id):
    """Insert a customer_event."""
    db_cursor.execute(
        "INSERT INTO customer_event "
        "(event_id, reservation_id) "
        "VALUES (%s, %s) ",
        (
            e_id, r_id
        )
    )


def insert_satisfaction(db_cursor, e_id, r_id, score):
    """Insert a satisfaction."""
    db_cursor.execute(
        "INSERT INTO satisfaction "
        "(event_id, reservation_id, score) "
        "VALUES (%s, %s, %s) ",
        (
            e_id, r_id, score
        )
    )


def insert_customer_order(db_cursor, r_id):
    """Insert a customer order."""
    db_cursor.execute(
        "INSERT INTO customer_order "
        "(reservation_id) "
        "VALUES (%s) "
        "RETURNING customer_order_id",
        (
            r_id,
        )
    )

    return db_cursor.fetchone()[0]


def insert_order_item(db_cursor, co_id, mi_id, quantity):
    """Insert a customer order."""
    db_cursor.execute(
        "INSERT INTO order_item "
        "(customer_order_id, menu_item_id, quantity) "
        "VALUES (%s, %s, %s)",
        (
            co_id, mi_id, quantity
        )
    )
