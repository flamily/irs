"""
Driver for managing staff records in the database.

This file contains a series of functions that manipulate and access records
in the datbase pertaining to management of staff and authentication.

Author: Andrew Pope
Date: 09/10/2018
"""
from passlib.hash import sha256_crypt

# TODO:
# - Create staff member
#   - Accepts a cleartext password, and is hashed with a method defined in here
# - List all staff
# - Check if password for username is correct
# - Get permission of staff member (based on username)
# - Get staff id from username
# - Get staff member based on username
# - Update Robin's example that creates staff members


def verify_password(db_conn, username, password):
    """Verify that the supplied staff password is correct.

    :param db_conn: A psycopg2 connection to the database.
    :param username: The username of the staff member.
    :param password: The password to verify against the database.
    :return: True if the user exists and the password is correct.
    :note: Will throw exception if staff member does not exist.
    """
    # Todo
    hash = 'foo'
    return sha256_crypt.verify(password, hash)


def list(db_conn):
    """Get a list of all menu items in the database.

    :param db_conn: A psycopg2 connection to the database.
    :return: A list of MenuItems.
    """
    # with db_conn.cursor() as curs:
    #     curs.execute(
    #         "SELECT * FROM menu_item"
    #     )
    #     menu_items = []
    #     for item in curs.fetchall():
    #         menu_items.append(
    #             MenuItem(
    #                 mi_id=item[0],
    #                 name=item[1],
    #                 description=item[2],
    #                 price=float(item[3])
    #             )
    #         )

    return []


def create_staff_member(db_conn, name, description, price):
    """Insert a menu items into the database.

    :param db_conn: A psycopg2 connection to the database.
    :param name: The name of the menu item.
    :param description: A description of the menu item.
    :param price: The price of the menu item.
    :return: Id of the newly created menu item.
    """
    # with db_conn.cursor() as curs:
    #     curs.execute(
    #         "INSERT INTO menu_item "
    #         "(name, description, price) "
    #         "VALUES (%s, %s, %s) "
    #         "RETURNING menu_item_id",
    #         (
    #             name, description, price
    #         )
    #     )
    #     mi_id = curs.fetchone()[0]
    #     db_conn.commit()
    password = sha256_crypt.encrypt("password")
    return 1
