"""
Driver for managing the restaurant table records in the database.

This file contains a series of functions that manipulate and access records
in the datbase pertaining to management of the restaurant.

Author: Andrew Pope
Date: 06/10/2018
"""
from irs.app.restaurant_table import (
    RestaurantTable, Event, Shape, Coordinate
)


def ready(db_conn):
    assert True


def maintain(db_conn):
    assert True


def ordered(db_conn):
    """Menu items etc??"""
    assert True


def paid(db_conn, table_id, staff_id):
    """...."""
    with db_conn.cursor() as curs:
        curs.execute(
            "INSERT INTO event "
            "(description, restaurant_table_id, staff_id) "
            "VALUES (%s, %s, %s) "
            "RETURNING event_id",
            (
                str(Event.paid), table_id, staff_id
            )
        )
    assert True


def applyConfirmation(db_conn, table_id, staff_id, party_size):
    """...."""
    # Inserts reservation, event??
    assert True


def overview(db_conn):
    """List of all the restaurant tables.

    :param db_conn: An active connection to the database.
    :return: Return a list of RestaurantTables.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT rt.*, et.description "
            "FROM restaurant_table rt "
            "JOIN event et on et.restaurant_table_id=rt.restaurant_table_id "  # noqa: E501
            "WHERE et.event_id = ("
            " SELECT e.event_id FROM event e "
            " WHERE e.restaurant_table_id = rt.restaurant_table_id "
            " ORDER BY event_dt desc LIMIT 1"
            ")"
        )

        rt_list = []
        for table in curs.fetchall():
            rt_list.append(
                RestaurantTable(
                    rt_id=table[0],
                    capacity=table[1],
                    coordinate=Coordinate(x=table[2], y=table[3]),
                    width=table[4],
                    height=table[5],
                    shape=Shape(table[6]),
                    latest_event=Event(table[7])
                )
            )

        return rt_list
