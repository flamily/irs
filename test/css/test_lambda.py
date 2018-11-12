"""
Test the CSS lambda

Author: Robin Wohlers-Reichel
Date: 11/11/2018
"""

import events.satisfaction_lambda as sl
import biz.css.manage_satisfaction as ms
import biz.manage_restaurant as mr
import biz.css.reduction as r
import biz.css.emotion_recognition as er
import pytest
import test.helper as h

# pylint: disable=no-member


def test_get_details():
    """
    Check the details are read from the filename
    """
    event = {'Records': [
        {
            's3': {
                'bucket': {
                    'name': 'css-bucket'
                },
                'object': {
                    'key': '2-3.img'
                }
            }
        }
    ]}
    bucket, key = sl.get_details(event)
    assert bucket == "css-bucket"
    assert key == "2-3.img"


def test_get_details_throw():
    """
    Correctly handle malformed filenames
    """
    event = {'Records': [
        {
            's3': {
                'no_bucket': {
                    'name': 'css-bucket'
                },
                'object': {
                    'key': '2-3.img'
                }
            }
        }
    ]}
    with pytest.raises(KeyError):
        sl.get_details(event)


def test_save_css_exception(mocker):
    """
    Do not eat database exceptions
    """
    mocker.patch('biz.css.manage_satisfaction.create_satisfaction')
    ms.create_satisfaction.side_effect = Exception('oh no')
    dodgy_pool = h.mock_db_pool(mocker)
    with pytest.raises(Exception) as execinfo:
        sl.save_css(dodgy_pool, 50, 11, 22)
    ms.create_satisfaction.assert_called_once_with(dodgy_pool.conn,
                                                   50,
                                                   11,
                                                   22)
    assert str(execinfo.value) == 'oh no'
    dodgy_pool.getconn.assert_called_once()
    dodgy_pool.putconn.assert_called_once()
    dodgy_pool.conn.commit.assert_not_called()
    dodgy_pool.conn.rollback.assert_called_once()


def test_save_css(mocker):
    """
    Saving css using correct biz methods
    """
    mocker.patch('biz.css.manage_satisfaction.create_satisfaction')
    dodgy_pool = h.mock_db_pool(mocker)
    sl.save_css(dodgy_pool, 50, 11, 22)
    ms.create_satisfaction.assert_called_once_with(dodgy_pool.conn,
                                                   50,
                                                   11,
                                                   22)
    dodgy_pool.getconn.assert_called_once()
    dodgy_pool.putconn.assert_called_once()
    dodgy_pool.conn.commit.assert_called_once()
    dodgy_pool.conn.rollback.assert_not_called()


def test_save_css_with_database(database_snapshot):
    """
    Saving css using db snapshot. check transaction etc
    """
    # setup db
    setup_conn = database_snapshot.getconn()
    t, staff = h.spoof_tables(setup_conn, 1)
    setup_conn.commit()
    (e1, r1) = mr.create_reservation(setup_conn, t[0], staff, 5)
    setup_conn.commit()
    database_snapshot.putconn(setup_conn)
    setup_conn = None

    # run test
    sl.save_css(database_snapshot, 50, e1, r1)

    # assert result
    conn = database_snapshot.getconn()
    try:
        score = ms.lookup_satisfaction(conn, e1, r1)
        assert score == 50
    finally:
        database_snapshot.putconn(conn)


def test_event_css(mocker):
    """
    Test whole thing through
    """
    mock_image_url = 'https://www.example.com/1-2.img'

    mocker.patch('events.satisfaction_lambda.generate_url')
    sl.generate_url.return_value = mock_image_url

    mocker.patch('events.satisfaction_lambda.css_for_image_at_url')
    sl.css_for_image_at_url.return_value = 50

    mocker.patch('events.satisfaction_lambda.save_css')
    mocker.patch('events.satisfaction_lambda.get_pool_lazy')
    sl.get_pool_lazy.return_value = 'super-legit-pool'

    event = {'Records': [
        {
            's3': {
                'bucket': {
                    'name': 'css-bucket'
                },
                'object': {
                    'key': '2-3.img'
                }
            }
        }
    ]}
    sl.calculate_css_from_image(event, None)

    sl.css_for_image_at_url.assert_called_once_with(mock_image_url)
    sl.save_css.assert_called_once_with('super-legit-pool', 50, 2, 3)


def test_event_css_bad_filename(mocker):
    """
    Bad filename means no call to Azure
    """
    mocker.patch('events.satisfaction_lambda.generate_url')
    event = {'Records': [
        {
            's3': {
                'bucket': {
                    'name': 'css-bucket'
                },
                'object': {
                    'key': 'wew.img'
                }
            }
        }
    ]}
    sl.calculate_css_from_image(event, None)
    sl.generate_url.assert_not_called()


def test_event_css_generate_failed(mocker):
    """
    Throws exception while generating URL
    """
    mocker.patch('events.satisfaction_lambda.generate_url')
    sl.generate_url.side_effect = Exception('oh no')
    mocker.patch('events.satisfaction_lambda.save_css')
    event = {'Records': [
        {
            's3': {
                'bucket': {
                    'name': 'css-bucket'
                },
                'object': {
                    'key': '1-2.img'
                }
            }
        }
    ]}
    with pytest.raises(Exception) as execinfo:
        sl.calculate_css_from_image(event, None)
    assert str(execinfo.value) == 'oh no'
    sl.save_css.assert_not_called()


def test_css_for_image_at_url(mocker):
    """
    Make sure we are getting features, then reducing
    """
    mocker.patch('biz.css.emotion_recognition.detect_from_url')

    mocker.patch('biz.css.reduction.apply_reduction')
    r.apply_reduction.return_value = 50

    result = sl.css_for_image_at_url('bingo')
    assert result == 50

    er.detect_from_url.assert_called_once()
    r.apply_reduction.assert_called_once()
