"""
Testing the flask endpoints for managing restaurant tables.

Author: Andrew Pope
Date: 25/10/2018
"""
import biz.manage_staff as ms
import biz.manage_restaurant as mg
from biz.staff import Permission
from biz.restaurant_table import Coordinate, Shape


def __spoof_user(client):
    """A user must be present and 'logged in'.

    :param client: The client running the flask app.
    :return: staff_id
    """
    pool = client.testing_db_pool
    conn = pool.getconn()
    s_id = ms.create_staff_member(
        conn, 'ldavid', 'password', ('Larry', 'David'),
        Permission.management
    )
    conn.commit()
    pool.putconn(conn)
    with client.session_transaction() as sess:
        sess['username'] = 'ldavid'

    return s_id


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
            mg.create_restaurant_table(
                conn, 3, Coordinate(x=0, y=3), 1,
                5, Shape.rectangle, staff_id
            )[0]
        )
    conn.commit()

    if reserve:
        for table in tables:
            mg.create_reservation(conn, table, staff_id, 2)
        conn.commit()

    pool.putconn(conn)
    return tables


def __make_params(table_id):
    """Make a simple payload for the table state form."""
    return dict(
        tableId=table_id,
        customerImg='nothingtoseehere',  # NB: Waiting for js image capture
    )


def test_index(client):
    """Test that tables endpoint can be hit."""
    __spoof_user(client)
    result = client.get('/tables')
    assert result.status_code == 200
    assert b'Restaurant Tables' in result.data


def test_list_available_tables(client):
    """Test that restaurant tables from db are being returned."""
    num_tables = 5
    sid = __spoof_user(client)
    tables = __spoof_tables(client, num_tables, sid)

    result = client.get('/tables')
    assert result.status_code == 200
    for table in tables:
        expect = 'data-tableId="{}"'.format(table)
        assert expect in str(result.data).replace(' ', '')


def test_list_reserved_tables(client):
    """Test that restaurant tables from db are being returned."""
    num_tables = 5
    sid = __spoof_user(client)
    tables = __spoof_tables(client, num_tables, sid, reserve=True)

    result = client.get('/tables')
    assert result.status_code == 200
    for table in tables:
        expect = 'data-tableId="{}"\\nclass="occupied-table'.format(table)
        assert expect in str(result.data).replace(' ', '')


def test_pay_after_reserved(client):
    """Test that a restaurant table can be paid for."""
    sid = __spoof_user(client)
    tid = __spoof_tables(client, 1, sid, reserve=True)[0]

    result = client.post(
        '/tables/pay/', data=__make_params(tid), follow_redirects=True
    )
    assert result.status_code == 200
    expect = 'unavailable'
    assert expect in str(result.data).replace(' ', '')


def test_ready_after_pay(client):
    """Test that a restaurant table can be made ready after being paid."""
    sid = __spoof_user(client)
    tid = __spoof_tables(client, 1, sid, reserve=True)[0]

    client.post(
        '/tables/pay/', data=__make_params(tid), follow_redirects=True
    )
    result = client.post(
        '/tables/ready/', data=__make_params(tid), follow_redirects=True
    )
    assert result.status_code == 200
    expect = 'available'
    assert expect in str(result.data).replace(' ', '')


def test_maintain_after_ready(client):
    """Test that a restaurant table can be marked for maintainence."""
    sid = __spoof_user(client)
    tid = __spoof_tables(client, 1, sid, reserve=True)[0]

    client.post(
        '/tables/pay/', data=__make_params(tid), follow_redirects=True
    )
    client.post(
        '/tables/ready/', data=__make_params(tid), follow_redirects=True
    )
    result = client.post(
        '/tables/maintain/', data=__make_params(tid), follow_redirects=True
    )
    assert result.status_code == 200
    expect = 'unavailable'
    assert expect in str(result.data).replace(' ', '')
