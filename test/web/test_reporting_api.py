import pytest
import json
import test.helper as h
import datetime


# "GET /api/reporting/Customer/date?dateString=2018-11-12 HTTP/1.1" 200 -
# "GET /api/reporting/Customer/date?dateString=2018-11-12&_=1542092099537 HTTP/1.1" 200 -


@pytest.mark.parametrize('url, err_msg', [
    # get_customer_report
    ('/api/reporting/Customer/not_date',
        'No date string provided'),
    ('/api/reporting/Customer/not_date?dateString=yew',
        'Invalid date format provided'),

    # get_staff_report
    ('/api/reporting/Staff/1/date',
        'No date string provided'),
    ('/api/reporting/Staff/1/not_date?dateString=yew',
        'Invalid date format provided'),
    ('/api/reporting/Staff/staff_id/date?dateString=yew',
        'Invalid staff_id provided'),

    # get_menu_score
    ('/api/reporting/Menu/1/date',
        'No date string provided'),
    ('/api/reporting/Menu/1/not_date?dateString=yew',
        'Invalid date format provided'),
    ('/api/reporting/Menu/staff_id/date?dateString=yew',
        'Invalid menu_id provided'),

    # staff_missing_error
    ('/api/reporting/Staff//date',
        'Missing staff_id from request'),

    # menu_missing_error
    ('/api/reporting/Menu//date',
        'Missing menu_id from request'),

])
def test_invalid_usage(client, url, err_msg):
    result = client.get(url)
    assert 400 == result.status_code
    assert err_msg == json.loads(result.data)['message']


@pytest.mark.parametrize('url, json_cardinality', [
    # json_cardinality is the number of items
    #   expected in a list at the key
    # None is a special case where we don't expect a list

    # get_customer_report
    ('/api/reporting/Customer/date?dateString=2018-01-01',
        {
            'average': None,
            'data': 3,
            'labels': 3,
            'scores': 3,
        }),

    # get_staff_report
    ('/api/reporting/Staff/1/date?dateString=2018-01-01',
        {
            'average': None,
            'data': 3,
            'labels': 3,
            'scores': 3,
        }),

    # get_menu_score
    ('/api/reporting/Menu/1/date?dateString=2018-01-01',
        {
            'average': None,
            'data': 3,
            'labels': 3,
            'scores': 3,
        }),

    # get_staff_and_menu_items
    ('/api/reporting/list_items',
        {
            'menu': 3,
            'staff': 1,
        }),

    # get_latest_entry_time
    ('/api/time/get_latest',
        {
            'data': None,
        }),

    # get_list_of_years
    ('/api/time/get_years',
        {
            'years': 1,
        }),
])
def test_endpoints(client, url, json_cardinality):
    pool = client.testing_db_pool
    db_connection = pool.getconn()
    t, staff = h.spoof_tables(db_connection, 3)
    db_connection.commit()

    h.spoof_menu_items(db_connection, 3)

    dt1 = datetime.datetime(2018, 1, 1)
    dt2 = datetime.datetime(2018, 1, 4)
    dt3 = datetime.datetime(2018, 1, 6)

    scores = [[40, 60, 80], [50, 55, 60], [40, 60, 80, 100]]

    h.spoof_satisfaction(
        db_connection,
        t,
        staff,
        [dt1, dt2, dt3],
        scores,
        [(1, 1)])
    db_connection.commit()
    pool.putconn(db_connection)

    result = client.get(url)
    assert 200 == result.status_code
    payload = json.loads(result.data)
    assert len(json_cardinality) == len(payload)
    for key, cardinality in json_cardinality.items():
        thing = payload.get(key, False)
        if cardinality is None:
            # we just check there is something
            assert thing
        else:
            # we check the length
            assert cardinality == len(thing)
