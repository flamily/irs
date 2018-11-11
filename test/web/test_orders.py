import biz.manage_menu as mm
import biz.manage_restaurant as mr
from test.web.helper import spoof_user, spoof_tables


def __spoof_menu_items(client):
    """Load a series of restaurant menu items.

    :param client: The client running the flask app.
    """
    pool = client.testing_db_pool
    conn = pool.getconn()
    menu_item = mm.create_menu_item(
        conn, 'food stuffs', 'good stuff', 2.99
    )
    conn.commit()

    pool.putconn(conn)
    return menu_item


def test_order_index(client):
    """Test that welcome endpoint can be hit."""
    spoof_user(client)
    result = client.get('/order/new', follow_redirects=True)
    assert result.status_code == 200
    assert b'Place An Order' in result.data


def test_order_menu_items(client):
    """Test that the new order page is populated with menu items."""
    spoof_user(client)
    menu_item = __spoof_menu_items(client)
    result = client.get('/order/new', follow_redirects=True)

    expect = 'data-menu_item_id="{}"'.format(menu_item)
    assert expect in str(result.data).replace(' ', '')


def test_order_tables(client):
    """Test that the new order page is populated tables."""
    num_tables = 1
    sid = spoof_user(client)
    table = spoof_tables(client, num_tables, sid, True)[0]
    result = client.get('/order/new', follow_redirects=True)
    expect = 'data-menu_table_id="{}"'.format(table)
    assert expect in str(result.data).replace(' ', '')


def test_order_created(client):
    """Test that an order can be created."""
    num_tables = 1
    sid = spoof_user(client)
    table = spoof_tables(client, num_tables, sid, True)[0]
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
    """Test that restaurant tables from db are being returned."""
    menu_items = list()
    num_tables = 1
    sid = spoof_user(client)
    table = spoof_tables(client, num_tables, sid, True)[0]
    menu_item = __spoof_menu_items(client)
    menu_items.append(tuple([menu_item, 1]))
    pool = client.testing_db_pool
    conn = pool.getconn()
    pool.putconn(conn)
    _, r_id, _ = mr.order(conn, menu_items, table, sid)
    result = client.get('/order/get?rid='+str(r_id))
    assert result.status_code == 200
