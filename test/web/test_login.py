import pytest
import urllib.parse
import biz.manage_staff as ms
from biz.staff import Permission

USERNAME = 'ldavid'
PASSWORD = 'prettygood'


@pytest.mark.parametrize('next_url, expect', [
    (False, ''),
    ('', ''),
    ('http://bad.com/good', ''),
    ('http://bad.com', ''),
    ('http://localhost/', 'http://localhost/'),
    ('http://localhost/good', 'http://localhost/good'),
])
def test_login_populate_redirect(client, next_url, expect):
    url = __make_next(next_url)
    form = '<input type=hidden value="{}" name=next>'
    form_next = form.format(expect).encode()

    result = client.get(url)
    assert result.status_code == 200
    assert form_next in result.data


@pytest.mark.parametrize('next_url, expect', [
    (False, 'http://localhost/'),
    ('', 'http://localhost/'),
    ('http://bad.com/good', 'http://localhost/'),
    ('http://bad.com', 'http://localhost/'),
    ('http://localhost/good', 'http://localhost/good'),
])
def test_login_redirect_location(client, next_url, expect):
    __spoof_user(client)
    params = __make_params(next_url)
    result = client.post('/login/', data=params)
    assert result.status_code == 302
    assert expect == result.location


def test_redirect_not_logged_in(client):
    endpoint_uri = client.get('/')
    assert endpoint_uri.status_code == 302
    assert '/login/?next=' in endpoint_uri.location


def test_login_empty(client):
    endpoint_uri = client.get('/login/')
    assert endpoint_uri.status_code == 200
    assert b'Login' in endpoint_uri.data


def test_login_sets_session_cookie(client):
    __spoof_user(client)
    params = __make_params()
    result = client.post('/login/', data=params)
    assert __get_setcookie(result, 'session')


def test_logout_resets_session_cookie(client):
    __spoof_user(client)
    params = __make_params()
    result = client.post('/login/', data=params, follow_redirects=True)
    assert result.status_code == 200

    result = client.post('/login/logout/', data=params)
    assert __get_setcookie(result, 'session') == ''


def test_login(client):
    __spoof_user(client)
    params = __make_params()
    result = client.post('/login/', data=params, follow_redirects=True)
    assert result.status_code == 200
    assert b'Dashboard' in result.data


def __spoof_user(client):
    """Insert the expected user into the database.

    :param client: The client running the flask app.
    :return: staff_id
    """
    pool = client.testing_db_pool
    conn = pool.getconn()
    s_id = ms.create_staff_member(
        conn, USERNAME, PASSWORD, ('Larry', 'David'),
        Permission.management
    )
    conn.commit()
    pool.putconn(conn)
    return s_id


def __make_params(next_url=False):
    if not next_url or next_url is False:
        return dict(
            username=USERNAME,
            password=PASSWORD
        )
    return dict(
        username=USERNAME,
        password=PASSWORD,
        next=next_url
    )


def __make_next(next_url):
    if not next_url or next_url is False:
        return '/login/'
    n = next_url.encode()
    e = urllib.parse.quote_plus(n)
    return '/login/?next=' + e


def __get_setcookie(response, name, default_value=None):
    from werkzeug.http import parse_cookie
    cookies = response.headers.getlist('Set-Cookie')
    ret = default_value
    for cookie in cookies:
        parsed = parse_cookie(cookie)
        val = parsed.get(name)
        if val is not None:
            # make sure we have exactly one match
            assert ret == default_value
            ret = val
            continue
    return ret
