import biz.manage_staff as ms
import biz.manage_restaurant as mr
import biz.manage_menu as mm
from biz.staff import Permission
from biz.restaurant_table import (Coordinate, Shape)
import biz.css.manage_satisfaction as mcss


def update_order_dt(db_conn, rid, dt):
    """Spoof an event's datetime.
    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "UPDATE customer_order "
            "SET order_dt = %s "
            "WHERE reservation_id = %s",
            (dt, rid)
        )
        db_conn.commit()


def spoof_satisfaction(db_conn, t, staff, dates, scores, menu_items=[]):
    # pylint: disable=dangerous-default-value
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    db_connection = db_conn
    for table, event_date, score in zip(t, dates, scores):
        ce1 = mr.create_reservation(db_connection, table, staff, 5)
        mcss.create_satisfaction(db_connection, score[0], ce1[0], ce1[1])

        orders = []
        for s in score[1:-1]:
            ce2 = mr.order(db_connection, menu_items, table, staff)
            mcss.create_satisfaction(db_connection, s, ce2[0], ce2[1])
            orders.append(ce2)

        ce3 = mr.paid(db_connection, table, staff)
        mcss.create_satisfaction(db_connection, score[-1], ce3[0], ce3[1])

        update_reservation_dt(db_connection, ce1[1], ce1[0], event_date)
        for order in orders:
            update_reservation_dt(
                db_connection,
                order[1],
                order[0],
                event_date)
        update_reservation_dt(db_connection, ce3[1], ce3[0], event_date)


# Functions for spoofing time
def update_event_dt(db_conn, eid, dt):
    """Spoof an event's datetime.

    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "UPDATE event "
            "SET event_dt = %s "
            "WHERE event_id = %s",
            (dt, eid)
        )
        db_conn.commit()


def update_reservation_dt(db_conn, rid, eid, dt):
    """Spoof a reservation's datetime.

    :param rid: The id of the reservation record to spoof.
    :param eid: The id of the event record to spoof.
    :param dt: The new datetime to spoof.
    """
    with db_conn.cursor() as curs:
        update_event_dt(db_conn, eid, dt)
        update_order_dt(db_conn, rid, dt)
        curs.execute(
            "UPDATE reservation "
            "SET reservation_dt = %s "
            "WHERE reservation_id = %s",
            (dt, rid)
        )
        db_conn.commit()


def spoof_menu_items(db_conn, n):
    """Load a series of menu_items.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: [mi1_id, mi2_id ... min_id]
    """
    items = []
    for i in range(0, n):
        items.append(
            mm.create_menu_item(
                db_conn, str(i), 'a description', i
            )
        )
    return items


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


def spoof_tables(db_conn, n, username='ldavid', first='Larry', last='David'):
    """Load a series of restaurant tables and a staff member.

    :param db_conn: A psycopg2 connection to the database.
    :param n: The number of restaurant_tables to create.
    :return: ([t1_id, t2_id ... tn_id], staff_id)
    """
    staff_id = ms.create_staff_member(
        db_conn, username, 'prettygood', (first, last),
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
    """
    Make a mock db pool to test commit/rollback being called
    """
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
