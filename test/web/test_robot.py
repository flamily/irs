import biz.manage_staff as ms
from biz.staff import Permission


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


def test_index(client):
    """Test that welcome endpoint can be hit."""
    __spoof_user(client)
    result = client.get('/robot')
    assert result.status_code == 200
    assert b'Welcome' in result.data


def test_party(client):
    """Test that select_party_size endpoint can be hit."""
    __spoof_user(client)
    result = client.get('/robot/party')
    assert result.status_code == 200
