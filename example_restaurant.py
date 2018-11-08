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
import time
from datetime import datetime, date, timedelta

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


def __database_connect():
    """Connect to the existing localhost database returning a psycopg2 conn."""
    conn = psycopg2.connect("user='postgres' host='localhost' port='5432'")
    return conn


# Functions for spoofing time
def __update_event_dt(conn, eid, dt):
    """Spoof an event's datetime."""
    with conn.cursor() as curs:
        curs.execute(
            "UPDATE event "
            "SET event_dt = %s "
            "WHERE event_id = %s",
            (dt, eid)
        )
        conn.commit()


def __update_reservation_dt(conn, rid, eid, dt):
    """Spoof a reservation's datetime."""
    with conn.cursor() as curs:
        __update_event_dt(conn, eid, dt)
        curs.execute(
            "UPDATE reservation "
            "SET reservation_dt = %s "
            "WHERE reservation_id = %s",
            (dt, rid)
        )
        conn.commit()


def __update_order_dt(conn, oid, eid, dt):
    """Spoof a customer order's datetime."""
    with conn.cursor() as curs:
        __update_event_dt(conn, eid, dt)
        curs.execute(
            "UPDATE customer_order "
            "SET order_dt = %s "
            "WHERE customer_order_id = %s",
            (dt, oid)
        )
        conn.commit()


def __setup_menu(conn):
    """Return menu item ids."""
    MENU.append(mgmenu.create_menu_item(
        conn, 'Lobster Bisque', 'Very tasty', 25.80
    ))
    MENU.append(mgmenu.create_menu_item(
        conn, 'Cheese toastie', 'Yummy!', 5.80
    ))
    MENU.append(mgmenu.create_menu_item(
        conn, 'Big Nut Latte', 'Wow much taste', 2.80
    ))
    MENU.append(mgmenu.create_menu_item(
        conn, 'Buger & Chips', 'Surf n Turf baby', 10.80
    ))
    conn.commit()


def __setup_staff(conn):
    """Create staff members and return their staff ids."""
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
    conn.commit()


def __setup_tables(conn, n):
    """Setup restaurant tables and return their (ids, capacity)."""
    tables = []
    creation_dts = []

    for _ in range(0, n):
        capacity = random.randint(1, 10)
        location = Coordinate(x=random.randint(0, 20), y=random.randint(0, 20))
        width = random.randint(1, capacity)
        height = random.randint(1, capacity)
        shape = random.choice(list(Shape))
        tid, eid = mgrest.create_restaurant_table(
            conn, capacity, location, width, height, shape, STAFF[0]
        )  # By default all tables are marked as 'ready'
        tables.append((tid, capacity))

        SPOOF_DATES['table_creation'].append(
            (eid, datetime.utcnow() + timedelta(weeks=-8))
        )  # Lets say that the tables were created 8 weeks ago

    conn.commit()
    return tables, creation_dts


def __generate_reservation(conn, tid, sid, table_capacity):
    """Generate reservation, returning (eid, rid, group_size)."""
    group_size = random.randint(1, table_capacity)
    eid, rid = mgrest.create_reservation(conn, tid, sid, group_size)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
    conn.commit()
    return (eid, rid, group_size)


def __generate_order(conn, tid, sid, group_size):
    """Generate a random order for the table, returning (eid, rid, oid)."""
    menu_items = []
    for _ in range(0, group_size):
        menu_items.append(
            (MENU[random.randint(0, len(MENU)-1)], random.randint(1, 3))
        )
    eid, rid, oid = mgrest.order(conn, menu_items, tid, sid)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
    conn.commit()
    return (eid, rid, oid)


def __pay_reservation(conn, tid, sid):
    """Pay for a reservation, returning (eid,rid)."""
    eid, rid = mgrest.paid(conn, tid, sid)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
    conn.commit()
    return (eid, rid)


def __customer_experience(conn, tid, sid, table_capacity, dt,
                          pay=False, make_ready=False):
    """Generate a restaurant 'customer experience' (reserve, order, pay)."""
    # Order 10-20mins after being seated
    order_dt = dt + timedelta(minutes=(random.randint(10, 20)))
    # Pay 30-120mins after ordering
    pay_dt = order_dt + timedelta(minutes=(random.randint(30, 120)))
    # Ready table 5-10mins after paying
    ready_dt = pay_dt + timedelta(minutes=(random.randint(5, 10)))

    # Create reservation and set the date
    event, rid, gsize = __generate_reservation(conn, tid, sid, table_capacity)
    SPOOF_DATES['reservation'].append((rid, event, dt))

    # Order
    event, _, order = __generate_order(conn, tid, sid, gsize)
    SPOOF_DATES['order'].append((order, event, order_dt))

    if pay:  # Optionally pay
        event, _ = __pay_reservation(conn, tid, sid)
        SPOOF_DATES['table_paid'].append((event, pay_dt))

        if make_ready:  # Optionally make ready after paying
            event = mgrest.ready(conn, tid, sid)
            SPOOF_DATES['table_paid'].append((event, ready_dt))
    conn.commit()


def __recent_restaurant_state(conn, tids):
    """Given a list of tables, initialise their current restaurant state."""
    for tid, capacity in tids:
        # Choose random staff member to do transaction
        sid = STAFF[random.randint(0, len(STAFF)-1)]

        # Choose a random action to apply to the table - start at 9am of today
        choice = random.randint(0, 3)
        exp_dt = datetime.utcnow().replace(hour=9, minute=1)
        if choice == 1:
            print("table ({}) setup : reserved and ordered".format(tid))
            __customer_experience(conn, tid, sid, capacity, exp_dt)
        elif choice == 2:
            print("table ({}) setup : reserved, ordered and paid".format(tid))
            __customer_experience(conn, tid, sid, capacity, exp_dt, True)
        elif choice == 3:
            print("table ({}) setup : maintainence".format(tid))
            mgrest.maintain(conn, tid, sid)
        else:
            print("table ({}) setup : ready".format(tid))
            continue  # Leave it be (available)


def __create_history(conn, tids):
    # For each table we want to generate a sordid history
    # (only 4 days worth)
    for tid, capacity in tids:
        for day in reversed(range(2, 6)):
            for hour in range(0, 5, random.randint(1, 3)):
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
                    conn, tid, sid, capacity, hist_dt, True, True
                )


def __apply_spoof_dates(conn):
    """Apply spoof dates after all necessary records have been created."""
    for reservation, event, spoof_dt in SPOOF_DATES['reservation']:
        __update_reservation_dt(conn, reservation, event, spoof_dt)

    for order, event, spoof_dt in SPOOF_DATES['order']:
        __update_order_dt(conn, order, event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_creation']:
        __update_event_dt(conn, event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_paid']:
        __update_event_dt(conn, event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_ready']:
        __update_event_dt(conn, event, spoof_dt)

    for event, spoof_dt in SPOOF_DATES['table_maintainence']:
        __update_event_dt(conn, event, spoof_dt)


if __name__ == "__main__":
    db_conn = __database_connect()
    print("...creating staff members...")
    __setup_staff(db_conn)
    print("...creating menu items...")
    __setup_menu(db_conn)
    print("...creating restaurant tables...")
    table_ids, creation_dts = __setup_tables(db_conn, 11)
    print("...spoofing restaurant history...")
    historic_dts = __create_history(db_conn, table_ids)
    print("...spoofing current restaurant state...")
    recent_dts = __recent_restaurant_state(db_conn, table_ids)
    print("...applying spoof dates for historic restaurant data...")
    __apply_spoof_dates(db_conn)

    db_conn.close()
