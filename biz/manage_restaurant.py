"""
Driver for managing the restaurant records in the database.

This file contains a series of functions that manipulate and access records
in the datbase pertaining to management of the restaurant.

Author: Andrew Pope
Date: 06/10/2018
"""
from irs.app.src.restaurant_table import (
    RestaurantTable, Event, Shape, Coordinate
)


def __create_event(db_curs, event, table_id, staff_id):
    """Create a table event in the database.

    :param db_curs: A psycopg2 cursor object.
    :param event: An instance of the Event enum.
    :param table_id: The table the event is occuring upon.
    :param staff_id: The id of the staff member making it hapen.
    :return: event_id.
    """
    db_curs.execute(
        "INSERT INTO event "
        "(description, restaurant_table_id, staff_id) "
        "VALUES (%s, %s, %s) "
        "RETURNING event_id",
        (
            str(event), table_id, staff_id
        )
    )
    return db_curs.fetchone()[0]


def __create_customer_event(db_curs, event_id, reservation_id):
    """Create a customer event in the database.

    :param db_curs: A psycopg2 cursor object.
    :param event_id: The responsible event_id.
    :param reservation_id: The reservation upon which the event occured at.
    """
    db_curs.execute(
        "INSERT INTO customer_event "
        "(event_id, reservation_id) "
        "VALUES (%s, %s) ",
        (
            event_id, reservation_id
        )
    )


def lookup_order(db_conn, reservation_id):
    """Return the order id of the reservation.

    :param db_conn: A psycopg2 connection to the database.
    :param reservation_id: The reservation id to lookup.
    :return: customer_order_id
    :note: Will throw exception if no customer order exists for reservation.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT co.customer_order_id "
            "FROM customer_order co "
            "WHERE co.reservation_id = %s",
            (reservation_id,)
        )

        return curs.fetchone()[0]


def order(db_conn, menu_items, table_id, staff_id):
    """Add a series of menu items to a reservation's order.

    :param db_conn: A psycopg2 connection to the database.
    :param menu_items: A list of [(menu_item_id, quantity)] to add to order.
    :param table_id: The id of the table to add too.
    :param staff_id: The id of the staff member facilitating the order.
    :return: (event_id, reservation_id, order_id) of the order event.
    """
    reservation_id = lookup_reservation(db_conn, table_id)

    try:
        order_id = lookup_order(db_conn, reservation_id)
    except TypeError:
        order_id = None  # The order has yet to exist

    with db_conn.cursor() as curs:
        if order_id is None:
            curs.execute(
                "INSERT INTO customer_order "
                "(reservation_id) "
                "VALUES (%s) "
                "RETURNING customer_order_id",
                (
                    reservation_id,
                )
            )
            order_id = curs.fetchone()[0]  # Create the order

        # Append each menu item to the order
        for menu_item_id, quantity in menu_items:
            curs.execute(
                "INSERT INTO order_item "
                "(customer_order_id, menu_item_id, quantity) "
                "VALUES (%s, %s, %s)",
                (
                    order_id, menu_item_id, quantity
                )
            )

        # Insert the attending event
        event_id = __create_event(curs, Event.attending, table_id, staff_id)
        __create_customer_event(curs, event_id, reservation_id)
    return (event_id, reservation_id, order_id)


def ready(db_conn, table_id, staff_id):
    """Mark a table as ready.

    :param db_conn: A psycopg2 connection to the database.
    :param table_id: Id of the restaurant table to mark as ready.
    :param staff_id: Id of the staff member responsible.
    :return: event_id of the ready event
    """
    with db_conn.cursor() as curs:
        event_id = __create_event(curs, Event.ready, table_id, staff_id)
    return event_id


def maintain(db_conn, table_id, staff_id):
    """Mark a table for maintainence.

    :param db_conn: A psycopg2 connection to the database.
    :param table_id: Id of the restaurant table to maintain.
    :param staff_id: Id of the staff member responsible.
    :return: event_id of the maintain event
    """
    with db_conn.cursor() as curs:
        event_id = __create_event(curs, Event.maintaining, table_id, staff_id)
    return event_id


def paid(db_conn, table_id, staff_id):
    """Pay for a reservation at a table.

    :param db_conn: A psycopg2 connection to the database.
    :param table_id: Id of the restaurant table to pay for.
    :param staff_id: Id of the staff member responsible.
    :return: (event_id, reservation_id) of the paid event.
    """
    reservation_id = lookup_reservation(db_conn, table_id)

    with db_conn.cursor() as curs:
        event_id = __create_event(curs, Event.paid, table_id, staff_id)
        __create_customer_event(curs, event_id, reservation_id)
    return (event_id, reservation_id)


def lookup_reservation(db_conn, table_id):
    """Return the reservation id of the currently occupied table.

    :param db_conn: A psycopg2 connection to the database.
    :param table_id: The table id to lookup.
    :return: reservation_id.
    :note: Will throw exception if no reservation exists for table.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT ce.reservation_id "
            "FROM customer_event ce "
            "JOIN event et on et.event_id=ce.event_id "
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

    :param db_conn: A psycopg2 connection to the database.
    :param table_id: Id of the restaurant table to book.
    :param staff_id: Id of the staff member responsible.
    :param group_size: Number of customers in reservation.
    :return: (event_id, reservation_id) of newly created reservation.
    """
    with db_conn.cursor() as curs:
        event_id = __create_event(curs, Event.seated, table_id, staff_id)
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
        __create_customer_event(curs, event_id, reservation_id)
    return (event_id, reservation_id)


def overview(db_conn):
    """List of all the restaurant tables.

    :param db_conn: A psycopg2 connection to the database.
    :return: Return a list of RestaurantTables.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT rt.*, et.description "
            "FROM restaurant_table rt "
            "JOIN event et on et.restaurant_table_id=rt.restaurant_table_id "
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

    :param db_conn: A psycopg2 connection to the database.
    :param table_id: Id of table to find.
    :return: A RestaurantTable or None.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT rt.*, et.description "
            "FROM restaurant_table rt "
            "JOIN event et on et.restaurant_table_id=rt.restaurant_table_id "
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


# pylint:disable=too-many-arguments
def create_restaurant_table(db_conn, capacity, coordinate, width, height,
                            shape, staff_id):
    """Insert a restaurant table and mark it as ready.

    :param db_conn: A psycopg2 connection to the database.
    :param capacity: The capacity of the table.
    :param coordinate: An instance of the named tuple Coordinate.
    :param width: The width of the table.
    :param height: The height of the table.
    :param shape: An instance of the Shape enum.
    :param staff_id: The id of the staff member creating the table.
    :return: The id of the created table.
    :note: This will start the table in the 'ready' state.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "INSERT INTO restaurant_table "
            "(capacity, x_pos, y_pos, width, height, shape) "
            "VALUES (%s, %s, %s, %s, %s, %s) "
            "RETURNING restaurant_table_id",
            (
                capacity,
                coordinate.x, coordinate.y,
                width,
                height,
                str(shape)
            )
        )
        rt_id = curs.fetchone()[0]
        __create_event(curs, Event.ready, rt_id, staff_id)  # Default event
    return rt_id


def put_satisfaction(db_conn, customer_event_id, score):
    """Create a satisfaction record for a customer event.

    :param db_conn: A psycopg2 connection to the database.
    :param customer_event_id: A tuple of (event_id, reservation_id).
    :param score: The satisfaction score.
    """
    (event_id, reservation_id) = customer_event_id
    with db_conn.cursor() as curs:
        curs.execute(
            "INSERT INTO satisfaction "
            "(event_id, reservation_id, score) "
            "VALUES (%s, %s, %s) ",
            (
                event_id, reservation_id, score
            )
        )
