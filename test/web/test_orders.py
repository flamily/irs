"""
Tests for Order interface

Author: Robin Wohlers-Reichel, David Niwczyk
Date: 14/11/2018
"""
import biz.manage_menu as mm
import biz.manage_restaurant as mr
from test.helper import spoof_user
from biz.restaurant_table import (Coordinate, Shape)


def __spoof_menu_items(client):
    """Load a series of restaurant menu items.

    :param client: The client running the flask app.
    :return: menu item which was created
    """
    pool = client.testing_db_pool
    conn = pool.getconn()
    menu_item = mm.create_menu_item(
        conn, 'food stuffs', 'good stuff', 2.99
    )
    conn.commit()
    pool.putconn(conn)
    return menu_item


def __spoof_tables(client, n, staff_id, reserve=False):
    """Load a series of restaurant tables.

    :param client: The client running the flask app.
    :param n: The number of restaurant_tables to create.
    :param staff_id: The id of the staff member creating the tables.
    :param reserve: Mark the tables as being reserved.
    :return: ([t1_id, t2_id ... tn_id])
    """
    pool = client.testing_db_pool
    conn = pool.getconn()
    tables = []
    for _ in range(0, n):
        tables.append(
            mr.create_restaurant_table(
                conn, 3, Coordinate(x=0, y=3), 1,
                5, Shape.rectangle, staff_id
            )[0]
        )
    conn.commit()

    if reserve:
        for table in tables:
            mr.create_reservation(conn, table, staff_id, 2)
        conn.commit()

    pool.putconn(conn)
    return tables


def test_order_index(client):
    """Test that welcome endpoint can be hit.

    :param client: The client running the flask app.
    """
    spoof_user(client)
    result = client.get('/order/new', follow_redirects=True)
    assert result.status_code == 200
    assert b'Place An Order' in result.data


def test_order_menu_items(client):
    """Test that the new order page is populated with menu items.

    :param client: The client running the flask app.
    """
    spoof_user(client)
    menu_item = __spoof_menu_items(client)
    result = client.get('/order/new', follow_redirects=True)
    expect = 'data-menu_item_id="{}"'.format(menu_item)
    assert expect in str(result.data).replace(' ', '')


def test_order_tables(client):
    """Test that the new order page is populated tables.

    :param client: The client running the flask app.
    """
    num_tables = 1
    sid = spoof_user(client)
    table = __spoof_tables(client, num_tables, sid, True)[0]
    result = client.get('/order/new', follow_redirects=True)
    expect = 'data-menu_table_id="{}"'.format(table)
    assert expect in str(result.data)


def test_order_created(client):
    """Test that an order can be created.

    :param client: The client running the flask app.
    """
    num_tables = 1
    sid = spoof_user(client)
    table = __spoof_tables(client, num_tables, sid, True)[0]
    menu_item = __spoof_menu_items(client)
    form = dict([('table_id', table), (menu_item, 1)])
    pool = client.testing_db_pool
    conn = pool.getconn()
    r_id = mr.lookup_reservation(conn, table)
    pool.putconn(conn)
    result = client.post('/order/new',
                         data=form,
                         follow_redirects=True)

    expect = 'data-reservation_id="{}"'.format(r_id)
    assert expect in str(result.data).replace(' ', '')


def test_list_menu_items(client):
    """Test that restaurant tables from db are being returned.

    :param client: The client running the flask app.
    """
    menu_items = list()
    num_tables = 1
    sid = spoof_user(client)
    table = __spoof_tables(client, num_tables, sid, True)[0]
    menu_item = __spoof_menu_items(client)
    menu_items.append(tuple([menu_item, 1]))
    pool = client.testing_db_pool
    conn = pool.getconn()
    _, r_id, _ = mr.order(conn, menu_items, table, sid)
    pool.putconn(conn)
    result = client.get('/order/get?rid='+str(r_id))
    assert result.status_code == 200
