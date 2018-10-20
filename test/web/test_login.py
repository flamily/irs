def test_login_empty(client):
    endpoint_uri = client.get('/login/')
    assert endpoint_uri.status_code == 200
    assert b'Login' in endpoint_uri.data


# def test_friends_add(client):
#     friend = b'bingo'
#     rv = client.post('/friend', data=dict(
#         name=friend
#     ), follow_redirects=True)
#     assert b'<li>' + friend + b'</li>' in rv.data


# def test_friends_redirect(client):
#     rv = client.get('/')
#     assert rv.status_code == 302
#     assert '/friend' in rv.location
# assert b'<a href="/friend">/friend</a>' in rv.data
