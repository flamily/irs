"""
Script to load the localhost database with a series of testing records.

This script assumes that a localhost instance of postgresql is running. It
generally expects the db to be clean.
E.g. `$ docker run --rm -p 5432:5432 irs_db`

Author: Andrew Pope
Date: 08/11/2018
"""
import psycopg2
import random
from datetime import (
    datetime, timedelta
)

import biz.manage_staff as mgstaff
import biz.manage_restaurant as mgrest
import biz.manage_menu as mgmenu
import biz.css.manage_satisfaction as mgsat
from biz.staff import Permission
from biz.restaurant_table import (Coordinate, Shape)


MENU = []
STAFF = []
SPOOF_DATES = {
    'reservation': [],
    'order': [],
    'table_creation': [],
    'table_paid': [],
    'table_ready': [],
    'table_maintainence': []
}
conn = None  # A psycopg2 connection


# Functions for spoofing time
def __update_event_dt(eid, dt):
    """Spoof an event's datetime.

    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with conn.cursor() as curs:
        curs.execute(
            "UPDATE event "
            "SET event_dt = %s "
            "WHERE event_id = %s",
            (dt, eid)
        )
        conn.commit()


def __update_reservation_dt(rid, eid, dt):
    """Spoof a reservation's datetime.

    :param rid: The id of the reservation record to spoof.
    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with conn.cursor() as curs:
        __update_event_dt(eid, dt)
        curs.execute(
            "UPDATE reservation "
            "SET reservation_dt = %s "
            "WHERE reservation_id = %s",
            (dt, rid)
        )
        conn.commit()


def __update_order_dt(oid, eid, dt):
    """Spoof a customer_order's datetime.

    :param oid: The id of the order record to spoof.
    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with conn.cursor() as curs:
        __update_event_dt(eid, dt)
        curs.execute(
            "UPDATE customer_order "
            "SET order_dt = %s "
            "WHERE customer_order_id = %s",
            (dt, oid)
        )
        conn.commit()


def __setup_menu():
    """Append a list of items to the restaurant menu."""
    milist = [
        ('Lobster Bisque', 'Very tasty', 25.80),
        ('Cheese toastie', 'Yummy!', 5.80),
        ('Big Nut Latte', 'Wow much taste', 2.80),
        ('Buger & Chips', 'Surf n Turf baby', 10.80)
    ]
    for mi in milist:
        MENU.append(mgmenu.create_menu_item(conn, mi[0], mi[1], mi[2]))
        print('menu item ({}) : ${}'.format(mi[0], mi[2]))
    conn.commit()


def __setup_staff():
    """Append a list of users to staff."""
    start_dt = datetime.utcnow() + timedelta(weeks=-9)
    slist = [
        ('ldavid', ('Larry', 'David'), Permission.management),
        ('jclank', ('Johnny', 'Clank'), Permission.robot),
        ('gcostanza', ('George', 'Costanza'), Permission.wait_staff)
    ]
    for s in slist:
        STAFF.append(mgstaff.create_staff_member(
            conn, s[0], s[0], s[1], s[2], start_dt
        ))
        print('user ({}) : password = {} , permission = {}'.format(
            s[0], s[0], s[2]
        ))
    conn.commit()


def __setup_tables(n):
    """Setup restaurant tables.

    :param n: The number of tables to setup.
    :return: A list of table ids and their capacity [(tid, capacity),...]
    """
    tables = []

    for _ in range(0, n):
        capacity = random.randint(2, 10)
        location = Coordinate(x=random.randint(0, 20), y=random.randint(0, 20))
        width = random.randint(1, capacity)
        height = random.randint(1, capacity)
        shape = random.choice(list(Shape))
        tid, eid = mgrest.create_restaurant_table(
            conn, capacity, location, width, height, shape, STAFF[0]
        )  # By default all tables are marked as 'ready'
        print('table ({}) : {} person capacity'.format(tid, capacity))
        tables.append((tid, capacity))
        SPOOF_DATES['table_creation'].append(
            (eid, datetime.utcnow() + timedelta(weeks=-8))
        )  # Lets say that the tables were created 8 weeks ago

    conn.commit()
    return tables


def __generate_reservation(tid, sid, table_capacity):
    """Create a reservation and spoof a satisfaction record.

    :param tid: The table id for the reservation.
    :param sid: The staff id of the responsible party.
    :param table_capacity: The capacity of the table.
    :return: (event id, reservation id, reservation size)
    """
    group_size = random.randint(1, table_capacity)
    eid, rid = mgrest.create_reservation(conn, tid, sid, group_size)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
    conn.commit()
    return (eid, rid, group_size)


def __generate_order(tid, sid, group_size):
    """Generate a random customer order of menu items, and spoof satisfaction.

    :param tid: The table id of the ordering party.
    :param sid: The staff id of the responsible party.
    :param group_size: The number of people in the reservation.
    :return: (event id, reservation id, order id)
    """
    menu_items = []
    for _ in range(0, group_size):
        menu_items.append(
            (MENU[random.randint(0, len(MENU)-1)], random.randint(1, 3))
        )
    eid, rid, oid = mgrest.order(conn, menu_items, tid, sid)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
    conn.commit()
    return (eid, rid, oid)


def __pay_reservation(tid, sid):
    """Pay for a reservation and spoof satisfaction.

    :param tid: The table id of the reservation.
    :param sid: The staff id of the responsible party.
    :return: (event id, reservation id)
    """
    eid, rid = mgrest.paid(conn, tid, sid)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
    conn.commit()
    return (eid, rid)


# pylint:disable=too-many-arguments
def __customer_experience(tid, sid, table_capacity, dt,
                          pay=False, make_ready=False):
    """Generate a 'customer experience'.

    This generates a series of events at a table including seating customers,
    ordering food, paying, and marking the table as ready again.

    :param tid: The table id that the experience occurs at.
    :param sid: The staff id of the responsible party.
    :param table_capacity: The person capacity of the table.
    :param dt: The datetime at which the experience occured (to be spoofed).
    :param pay: Indicate if the reservation should be paid for.
    :param make_ready: Indicate if the table should be marked as ready
                       after being paid for.
    """
    # Order 10-20mins after being seated
    order_dt = dt + timedelta(minutes=(random.randint(10, 20)))
    # Pay 30-120mins after ordering
    pay_dt = order_dt + timedelta(minutes=(random.randint(30, 120)))
    # Ready table 5-10mins after paying
    ready_dt = pay_dt + timedelta(minutes=(random.randint(5, 10)))

    # Create reservation and set the date
    sid = STAFF[random.randint(0, len(STAFF)-1)]
    event, rid, gsize = __generate_reservation(tid, sid, table_capacity)
    SPOOF_DATES['reservation'].append((rid, event, dt))

    # Order
    sid = STAFF[random.randint(0, len(STAFF)-1)]
    event, _, order = __generate_order(tid, sid, gsize)
    SPOOF_DATES['order'].append((order, event, order_dt))

    if pay:  # Optionally pay
        sid = STAFF[random.randint(0, len(STAFF)-1)]
        event, _ = __pay_reservation(tid, sid)
        SPOOF_DATES['table_paid'].append((event, pay_dt))

        if make_ready:  # Optionally make ready after paying
            sid = STAFF[random.randint(0, len(STAFF)-1)]
            event = mgrest.ready(conn, tid, sid)
            SPOOF_DATES['table_paid'].append((event, ready_dt))
    conn.commit()


def __recent_restaurant_state(tids):
    """Given a list of tables, initialise the most recent state of the retaurant.

    :param tids: A list of all the table ids (and person capacity)
                 in the restaurant. Of the form [(table id, capacity), ...]
    """
    for tid, capacity in tids:

        # Choose a random action to apply to the table
        choice = random.randint(0, 3)
        now = datetime.utcnow()
        if choice == 1:
            start_dt = now + timedelta(hours=-1)
            print("table ({}) setup : reserved and ordered".format(tid))
            # Choose random staff member to do transaction
            sid = STAFF[random.randint(0, len(STAFF)-1)]
            __customer_experience(tid, sid, capacity, start_dt)
        elif choice == 2:
            start_dt = now + timedelta(hours=-3)
            print("table ({}) setup : reserved, ordered and paid".format(tid))
            # Choose random staff member to do transaction
            sid = STAFF[random.randint(0, len(STAFF)-1)]
            __customer_experience(tid, sid, capacity, start_dt, True)
        elif choice == 3:
            start_dt = now + timedelta(minutes=-30)
            print("table ({}) setup : maintainence".format(tid))
            # Choose random staff member to do transaction
            sid = STAFF[random.randint(0, len(STAFF)-1)]
            event = mgrest.maintain(conn, tid, sid)
            SPOOF_DATES['table_maintainence'].append((event, start_dt))
        else:
            print("table ({}) setup : ready".format(tid))
            continue  # Leave it be (available)


def __create_history(tids):
    """Given a list of tables, initialise a sordid history of customer experiences.

    This currently generates a history of customer experiences at each table,
    4 days into the past.

    :param tids: A list of all the table ids (and person capacity)
                 in the restaurant. Of the form [(table id, capacity), ...]
    """
    # For each table we want to generate a sordid history
    # (only 4 days worth)
    for tid, capacity in tids:
        for day in reversed(range(1, 6)):
            for hour in range(0, 8, random.randint(1, 3)):
                # Choose a random staff memeber
                sid = STAFF[random.randint(0, len(STAFF)-1)]
                # Generate the hour of the day in which the table was seated
                hist_dt = datetime.utcnow().replace(hour=9, minute=0) + \
                    timedelta(
                        days=-day, hours=hour,
                        minutes=random.randint(1, 59)
                    )
                # Create the customer experience and append the historic dates
                __customer_experience(
                    tid, sid, capacity, hist_dt, True, True
                )


def __apply_spoof_dates():
    """Apply spoof dates after all necessary records have been created."""
    for reservation, event, spoof_dt in SPOOF_DATES['reservation']:
        __update_reservation_dt(reservation, event, spoof_dt)

    for order, event, spoof_dt in SPOOF_DATES['order']:
        __update_order_dt(order, event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_creation']:
        __update_event_dt(event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_paid']:
        __update_event_dt(event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_ready']:
        __update_event_dt(event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_maintainence']:
        __update_event_dt(event, spoof_dt)


if __name__ == "__main__":
    conn = psycopg2.connect("user='postgres' host='localhost' port='5432'")
    print("...creating staff members...")
    __setup_staff()
    print("...creating menu items...")
    __setup_menu()
    print("...creating restaurant tables...")
    table_ids = __setup_tables(11)
    print("...spoofing restaurant history...")
    __create_history(table_ids)
    print("...spoofing current restaurant state...")
    __recent_restaurant_state(table_ids)
    print("...applying spoof dates for historic restaurant data...")
    __apply_spoof_dates()

    conn.close()
