import biz.manage_staff as ms
import biz.manage_restaurant as mg
from biz.staff import Permission
from biz.restaurant_table import Coordinate, Shape


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


def spoof_tables(client, n, staff_id, reserve=False):
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
