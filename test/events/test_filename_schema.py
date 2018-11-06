"""
These tests check the filename schema generation for blob storage.

Author: Andrew Pope
Date: 06/11/2018
"""
import pytest
import events.satisfaction_lambda as sl


@pytest.mark.parametrize('event_id, reservation_id, expect', [
    (1, 2, '1-2.img'),
    (10, 4, '10-4.img'),
    (100000, 20000, '100000-20000.img'),
])
def test_construct_filename(event_id, reservation_id, expect):
    fn = sl.construct_filename(event_id, reservation_id)
    assert expect in fn


@pytest.mark.parametrize('event_id, reservation_id, filename', [
    (1, 2, '1-2.img'),
    (10, 4, '10-4.img'),
    (5, 3, '5-3'),
    (100000, 20000, '100000-20000.img'),
])
def test_deconstruct_filename(event_id, reservation_id, filename):
    eid, rid = sl.deconstruct_filename(filename)
    assert eid == event_id
    assert rid == reservation_id


@pytest.mark.parametrize('event_id, reservation_id', [
    (10.5, 6.2),
    ('dog', 'hair'),
    (1, 0.1),
    (22.5, 1)
])
def test_bad_input(event_id, reservation_id):
    with pytest.raises(TypeError):
        sl.construct_filename(event_id, reservation_id)


@pytest.mark.parametrize('filename', [
    ('dog-hair.img'),
    ('whatisthis'),
    ('10-man.img'),
])
def test_bad_filename(filename):
    with pytest.raises(ValueError):
        sl.deconstruct_filename(filename)
