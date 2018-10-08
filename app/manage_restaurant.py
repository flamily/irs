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


def ordered(db_conn):
    """Menu items etc??"""
    assert True


def maintain(db_conn, table_id, staff_id):
    """Mark a table for maintainence.

    :param table_id: Id of the restaurant table to book.
    :param staff_id: Id of the staff member who made the reservation.
    :return: event_id of the maintain event
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "INSERT INTO event "
            "(description, restaurant_table_id, staff_id) "
            "VALUES (%s, %s, %s) "
            "RETURNING event_id",
            (
                str(Event.maintaining), table_id, staff_id
            )
        )
        event_id = curs.fetchone()[0]
        db_conn.commit()
    return event_id


def paid(db_conn, table_id, staff_id):
    """Pay for a reservation at a table.

    :param table_id: Id of the restaurant table to book.
    :param staff_id: Id of the staff member who made the reservation.
    :return: (event_id, reservation_id) of the paid event.
    """
    reservation_id = lookup_reservation(db_conn, table_id)

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
        event_id = curs.fetchone()[0]
        curs.execute(
            "INSERT INTO customer_event "
            "(event_id, reservation_id) "
            "VALUES (%s, %s) ",
            (
                event_id, reservation_id
            )
        )
        db_conn.commit()
    return (event_id, reservation_id)


def lookup_reservation(db_conn, table_id):
    """Return the reservation id of the currently occupied table.

    :param table_id: The table id to lookup.
    :return: reservation_id or None (if not occupied).
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT ce.reservation_id "
            "FROM customer_event ce "
            "JOIN event et on et.event_id=ce.event_id "  # noqa: E501
            "WHERE et.event_id = ("
            " SELECT e.event_id FROM event e "
            " WHERE e.restaurant_table_id = %s "
            " ORDER BY event_dt desc LIMIT 1"
            ") "
            "AND et.description in ('seated', 'attending')",
            (table_id,)
        )

        return curs.fetchone()[0]


def create_reservation(db_conn, table_id, staff_id, group_size):
    """Create a reservation at a table.

    :param table_id: Id of the restaurant table to book.
    :param staff_id: Id of the staff member who made the reservation.
    :param group_size: Number of customer's in reservation.
    :return: (event_id, reservation_id) of newly created reservation.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "INSERT INTO event "
            "(description, restaurant_table_id, staff_id) "
            "VALUES (%s, %s, %s) "
            "RETURNING event_id",
            (
                str(Event.seated), table_id, staff_id
            )
        )
        event_id = curs.fetchone()[0]
        curs.execute(
            "INSERT INTO reservation "
            "(group_size) "
            "VALUES (%s) "
            "RETURNING reservation_id",
            (
                group_size,
            )
        )
        reservation_id = curs.fetchone()[0]
        curs.execute(
            "INSERT INTO customer_event "
            "(event_id, reservation_id) "
            "VALUES (%s, %s) ",
            (
                event_id, reservation_id
            )
        )
        db_conn.commit()

    return (event_id, reservation_id)


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


def get_table(db_conn, table_id):
    """Get details for a specifc restaurant table.

    :param db_conn: An active connection to the database.
    :param table_id: Id of table to find
    :return: A RestaurantTable.
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
            ") "
            "AND rt.restaurant_table_id = %s",
            (table_id,)
        )
        table = curs.fetchone()
        return RestaurantTable(
            rt_id=table[0],
            capacity=table[1],
            coordinate=Coordinate(x=table[2], y=table[3]),
            width=table[4],
            height=table[5],
            shape=Shape(table[6]),
            latest_event=Event(table[7])
        )
