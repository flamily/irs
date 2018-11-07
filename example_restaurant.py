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
import biz.manage_staff as mgstaff
import biz.manage_restaurant as mgrest
import biz.manage_menu as mgmenu
import biz.css.manage_satisfaction as mgsat
from biz.staff import Permission
from biz.restaurant_table import (Coordinate, Shape)


MENU = []
STAFF = []


def __database_connect():
    """Connect to the existing localhost database returning a psycopg2 conn."""
    conn = psycopg2.connect("user='postgres' host='localhost' port='5432'")
    return conn


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
    slist = [
        ('ldavid', ('Larry', 'David'), Permission.management, None),
        ('jclank', ('Johnny', 'Clank'), Permission.robot, None),
        ('gcostanza', ('George', 'Costanza'), Permission.wait_staff, None)
    ]
    for s in slist:
        STAFF.append(mgstaff.create_staff_member(
            conn, s[0], s[0], s[1], s[2], s[3]
        ))
    conn.commit()


def __setup_tables(conn, n):
    """Setup restaurant tables and return their (ids, capacity)."""
    tables = []
    for _ in range(0, n):
        capacity = random.randint(1, 10)
        location = Coordinate(x=random.randint(0, 20), y=random.randint(0, 20))
        width = random.randint(1, capacity)
        height = random.randint(1, capacity)
        shape = random.choice(list(Shape))
        tid = mgrest.create_restaurant_table(
            conn, capacity, location, width, height, shape, STAFF[0]
        )  # By default all tables are marked as 'ready'
        tables.append((tid, capacity))
    conn.commit()
    return tables


def __seat_customers(conn, tid, sid, table_capacity, pay=False):
    """Create a reservation for table and order some food!."""
    group_size = random.randint(1, table_capacity)
    eid, rid = mgrest.create_reservation(conn, tid, sid, group_size)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)

    menu_items = []
    for _ in range(0, group_size):
        menu_items.append(
            (MENU[random.randint(0, len(MENU)-1)], random.randint(1, 3))
        )
    eid, rid, _ = mgrest.order(conn, menu_items, tid, sid)
    mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
    conn.commit()

    if pay:
        eid, rid = mgrest.paid(conn, tid, sid)
        mgsat.create_satisfaction(conn, random.randint(0, 100), eid, rid)
        conn.commit()


def __setup_current_table_states(conn, tids):
    """Given a list of tables, initialise their current restaurant state."""
    for tid, capacity in tids:
        # Choose random staff member to do transaction
        sid = STAFF[random.randint(0, len(STAFF)-1)]

        # Choose a random action to apply to the table
        choice = random.randint(0, 3)
        if choice == 1:
            # Table is currently reserved and occupied
            __seat_customers(conn, tid, sid, capacity)
            print("active setup tid={} : reserved and ordered".format(tid))
        elif choice == 2:
            # Table has been reserved, occupied and then paid for
            __seat_customers(conn, tid, sid, capacity, True)
            print("active setup tid={} : ordered and paid".format(tid))
        elif choice == 3:
            # Table has been moved to maintainence mode
            mgrest.maintain(conn, tid, sid)
            print("active setup tid={} : maintainence".format(tid))
        else:
            print("active setup tid={} : ready".format(tid))
            continue  # Leave it be (available)


if __name__ == "__main__":
    conn = __database_connect()
    __setup_staff(conn)
    __setup_menu(conn)
    tids = __setup_tables(conn, 11)
    __setup_current_table_states(conn, tids)

    conn.close()
