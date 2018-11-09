"""
Testing for web error codes.

Author: Andrew Pope
Date: 06/11/2018
"""
from test.web.helper import spoof_user


def test_404(client):
    """Test that the 404 endpoint gets exercised."""
    result = client.get('/very-wrong')
    assert result.status_code == 404
    assert b'Page not found.' in result.data


def test_500(client):
    """Test that the 500 endpoint gets exercised."""
    # Attempt to get an endpoint that's only for posting!
    result = client.get(
        '/tables/pay/', data=dict(), follow_redirects=True
    )
    assert result.status_code == 500
    assert b'Something went wrong!' in result.data


def test_400(client):
    """Test that the 400 endpoint gets exercised."""
    # Attempt to post without any data
    spoof_user(client)
    result = client.post(
        '/robot/table/reserve', data=dict(
            table_id=2
        )
    )
    assert result.status_code == 400
    assert b'Something went wrong!' in result.data
