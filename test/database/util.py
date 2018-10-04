"""
A collection of database utility functions for testing.

Author: Andrew Pope
Date: 04/10/2018
"""


def insert_staff_record(db_cursor, username, permission):
    """Insert a record to the database."""
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
