import events.satisfaction_lambda as sl
import biz.css.manage_satisfaction as ms
import biz.css.reduction as r
import biz.css.emotion_recognition as er
import pytest


def test_get_details():
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
        bucket, key = sl.get_details(event)


def test_save_css_exception(mocker):
    class MockPool():
        def __init__(self):
            self.getconn = mocker.stub(name='getconn_stub')
            self.getconn.return_value = 'super-legit-conn'
            self.putconn = mocker.stub(name='putconn_stub')
    mocker.patch('biz.css.manage_satisfaction.create_satisfaction')
    ms.create_satisfaction.side_effect = Exception('oh no')
    dodgy_pool = MockPool()
    with pytest.raises(Exception) as execinfo:
        sl.save_css(dodgy_pool, 50, 11, 22)
    ms.create_satisfaction.assert_called_once_with('super-legit-conn',
                                                    50,
                                                    11,
                                                    22)
    assert 'oh no' == str(execinfo.value)
    dodgy_pool.getconn.assert_called_once()
    dodgy_pool.putconn.assert_called_once()


def test_save_css(mocker):
    class MockPool():
        def __init__(self):
            self.getconn = mocker.stub(name='getconn_stub')
            self.getconn.return_value = 'super-legit-conn'
            self.putconn = mocker.stub(name='putconn_stub')
    mocker.patch('biz.css.manage_satisfaction.create_satisfaction')
    dodgy_pool = MockPool()
    sl.save_css(dodgy_pool, 50, 11, 22)
    ms.create_satisfaction.assert_called_once_with('super-legit-conn',
                                                   50,
                                                   11,
                                                   22)
    dodgy_pool.getconn.assert_called_once()
    dodgy_pool.putconn.assert_called_once()


def test_event_css(mocker):
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
    sl.customer_satisfaction(event, None)

    sl.css_for_image_at_url.assert_called_once_with(mock_image_url)
    sl.save_css.assert_called_once_with('super-legit-pool', 50, 2, 3)


def test_event_css_bad_filename(mocker):
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
    sl.customer_satisfaction(event, None)
    sl.generate_url.assert_not_called()


def test_event_css_generate_failed(mocker):
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
        sl.customer_satisfaction(event, None)
    assert 'oh no' == str(execinfo.value)
    sl.save_css.assert_not_called()


def test_css_for_image_at_url(mocker):
    mocker.patch('biz.css.emotion_recognition.detect_from_url')

    mocker.patch('biz.css.reduction.apply_reduction')
    r.apply_reduction.return_value = 50

    result = sl.css_for_image_at_url('bingo')
    assert result == 50

    er.detect_from_url.assert_called_once()
    r.apply_reduction.assert_called_once()
