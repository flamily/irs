def test_friends_empty(client):
    rv = client.get('/friend')
    assert b'<ul>\n        \n        </ul>' in rv.data


def test_friends_add(client):
    friend = b'bingo'
    rv = client.post('/friend', data=dict(
        name=friend
    ), follow_redirects=True)
    assert b'<li>' + friend + b'</li>' in rv.data


## Deprecated since routing has been updated as '/' should be directing to index.
#def test_friends_redirect(client):
#    rv = client.get('/friend')
#    assert rv.status_code == 302
#    assert '/friend' in rv.location
#    assert b'<a href="/friend">/friend</a>' in rv.data
