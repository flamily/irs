import pytest
import biz.manage_staff as ms
from biz.staff import Permission
from biz.manage_restaurant import create_restaurant_table
from biz.restaurant_table import (
    Shape, Coordinate
)
from test.web.helper import spoof_user


def __spoof_user(client):
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


def test_tables(client):
    """Test that welcome endpoint can be hit."""
    __spoof_user(client)
    result = client.get('/robot/tables')
    assert result.status_code == 200
    assert b'Robot- Select Tables' in result.data


def test_index(client):
    """Test that welcome endpoint can be hit."""
    spoof_user(client)
    result = client.get('/robot')
    assert result.status_code == 200
    assert b'Welcome' in result.data


def test_party_size(client):
    """Test that select_party_size endpoint can be hit."""
    spoof_user(client)
    result = client.get('/robot/party')
    assert result.status_code == 200


def test_table(client):
    """Test that robot_table endpoint can be hit."""
    spoof_user(client)
    result = client.get('/robot/table')
    assert result.status_code == 200


def test_full(client):
    """Test that robot-table-full endpoint can be hit."""
    spoof_user(client)
    result = client.get('/robot/full')
    assert result.status_code == 200


def test_proceed(client):
    """Test that table-confirmation endpoint can be hit."""
    spoof_user(client)
    result = client.get('/robot/proceed')
    assert result.status_code == 200


@pytest.mark.parametrize('status_code, form', [
    (200, dict(
        group_size=1,
        photo='bingo',
    )),
    (400, dict(
        group_size=1,
    )),
    (400, dict(
        photo='bingo',
    ))
])
def test_reserve(client, status_code, form):
    """Test that robot-table-full endpoint can be hit."""
    sid = spoof_user(client)
    c = Coordinate(x=0, y=3)
    pool = client.testing_db_pool
    conn = pool.getconn()
    tid, _ = create_restaurant_table(conn, 10, c, 1, 5, Shape.rectangle, sid)
    conn.commit()
    pool.putconn(conn)

    form['table_id'] = tid

    result = client.post('/robot/table/reserve',
                         data=form,
                         follow_redirects=True)
    print(dir(result))
    print(result.location)
    assert result.status_code == status_code
