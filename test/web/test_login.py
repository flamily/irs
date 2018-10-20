import pytest
import urllib.parse


@pytest.mark.parametrize('next, expect', [
    (False,                   ''),
    ('',                      ''),
    ('http://bad.com/good',   ''),
    ('http://bad.com',        ''),
    ('http://localhost/',     'http://localhost/'),
    ('http://localhost/good', 'http://localhost/good'),
])
def test_login_populate_redirect(client, next, expect):
    url = __make_next(next)
    form = '<input type=hidden value="{}" name=next>'
    form_next = form.format(expect).encode()

    result = client.get(url)
    assert result.status_code == 200
    assert form_next in result.data


@pytest.mark.parametrize('next, expect', [
    (False,                   'http://localhost/'),
    ('',                      'http://localhost/'),
    ('http://bad.com/good',   'http://localhost/'),
    ('http://bad.com',        'http://localhost/'),
    ('http://localhost/good', 'http://localhost/good'),
])
def test_login_redirect_location(client, next, expect):
    params = __make_params(next)
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
    params = __make_params()
    result = client.post('/login/', data=params)
    assert len(__get_setcookie(result, 'session')) > 0


def test_logout_resets_session_cookie(client):
    params = __make_params()
    result = client.post('/login/', data=params, follow_redirects=True)
    assert result.status_code == 200
    result = client.post('/login/logout/', data=params)
    assert '' == __get_setcookie(result, 'session')


def test_login(client):
    params = __make_params()
    result = client.post('/login/', data=params, follow_redirects=True)
    assert result.status_code == 200
    assert b'Dashboard' in result.data


def __make_params(next=False):
    if not next or next is False:
        return dict(
            email='me@email.com',
            password='petemcgee'
        )
    return dict(
        email='me@email.com',
        password='petemcgee',
        next=next
    )


def __make_next(next):
    if not next or next is False:
        return '/login/'
    n = next.encode()
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
