from biz.manage_restaurant import (
    create_restaurant_table,
)
from biz.restaurant_table import (
    Shape, Coordinate
)
import pytest
from test.helper import spoof_user


def test_index(client):
    """Test that welcome endpoint can be hit."""
    sid = spoof_user(client)
    pool = client.testing_db_pool
    conn = pool.getconn()
    conn.commit()
    pool.putconn(conn)

    table_full_result = client.get('/robot')
    assert table_full_result.status_code == 302

    create_restaurant_table(
        conn, 2,
        Coordinate(x=0, y=3),
        1, 5,
        Shape.rectangle,
        sid
    )
    table_available_result = client.get('/robot')
    assert table_available_result.status_code == 200
    assert b'Welcome' in table_available_result.data


def test_party_size(client):
    """Test that select_party_size endpoint can be hit."""
    spoof_user(client)
    result = client.get('/robot/party')
    assert result.status_code == 200


def test_table(client):
    """Test that robot_table endpoint can be hit."""
    sid = spoof_user(client)
    pool = client.testing_db_pool
    conn = pool.getconn()
    conn.commit()
    pool.putconn(conn)

    no_tables_available_result = client.get('/robot/table?people=1')
    assert no_tables_available_result.status_code == 302

    create_restaurant_table(
        conn, 2,
        Coordinate(x=0, y=3),
        1, 5,
        Shape.rectangle,
        sid
    )
    table_available_result = client.get('/robot/table?people=2')
    assert table_available_result.status_code == 200


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

    result = client.post(
        '/robot/table/reserve',
        data=form,
        follow_redirects=True
    )
    print(dir(result))
    print(result.location)
    assert result.status_code == status_code
