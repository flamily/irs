"""
Tests reporting endpoints used for JSON data collation

Author: Robin Wohlers-Reichel
Date: 13/11/2018
"""


import pytest
import json
import test.helper as h


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
    """Tests the InvalidUsage error handling
    :param client: pytest fixture encompassing a flask client
    :param url: The routing URL to test
    :param err_msg: The expected error message response"""
    result = client.get(url)
    assert result.status_code == 400
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
    """Tests all endpoints using a predefined dataset for the database
    :param client: pytest fixture encompassing a flask client
    :param url: The routing url to test
    :param json_cardinality: The data structure expected from the response"""
    db_connection = client.testing_db_pool.getconn()
    h.spoof_system_for_css(db_connection)
    client.testing_db_pool.putconn(db_connection)

    result = client.get(url)
    assert result.status_code == 200
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
