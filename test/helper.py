import biz.manage_staff as ms
import biz.manage_restaurant as mr
from biz.staff import Permission
from biz.restaurant_table import (Coordinate, Shape)


def spoof_user(client):
    """A user must be present and 'logged in'.

    :param client: The client running the flask app.
    :return: staff_id
    """
    pool = client.testing_db_pool
    conn = pool.getconn()
    s_id = ms.create_staff_member(
        conn, 'rrobot', 'password', ('Roberto', 'Robot'),
        Permission.robot
    )
    conn.commit()
    pool.putconn(conn)
    with client.session_transaction() as sess:
        sess['username'] = 'rrobot'
    return s_id


def spoof_tables(db_conn, n):
    """Load a series of restaurant tables and a staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: ([t1_id, t2_id ... tn_id], staff_id)
    """
    staff_id = ms.create_staff_member(
        db_conn, 'ldavid', 'prettygood', ('Larry', 'David'),
        Permission.wait_staff
    )

    tables = []
    for _ in range(0, n):
        tables.append(
            mr.create_restaurant_table(
                db_conn, 2, Coordinate(x=0, y=3), 1,
                5, Shape.rectangle, staff_id
            )[0]
        )
    return (tables, staff_id)


def mock_db_pool(mocker):
    # pylint: disable=too-few-public-methods
    class MockConn():
        def __init__(self):
            self.rollback = mocker.stub(name='conn_rollback')
            self.commit = mocker.stub(name='conn_commit')

    class MockPool():
        def __init__(self):
            self.conn = MockConn()
            self.getconn = mocker.stub(name='getconn_stub')
            self.getconn.return_value = self.conn
            self.putconn = mocker.stub(name='putconn_stub')
    
    return MockPool()
