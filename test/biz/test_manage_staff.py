"""
These tests check the staff manager.

Author: Andrew Pope
Date: 09/10/2018
"""
import datetime
import psycopg2
from passlib.hash import sha256_crypt
import biz.manage_staff as ms
from biz.staff import (Staff, Permission)


def test_create_member(database_snapshot):
    """Create a staff member."""
    with database_snapshot.getconn() as conn:
        s_id = ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )

        member = ms.get_staff_member(conn, 'ldavid')
        assert member.s_id == s_id
        assert member.permission == Permission.wait_staff
        assert member.first_name == 'Larry'
        assert member.last_name == 'David'
        assert member.hashed_password != 'prettygood'
        assert sha256_crypt.verify('prettygood', member.hashed_password)


def test_lookup_member_id(database_snapshot):
    """Create a staff member."""
    with database_snapshot.getconn() as conn:
        s1 = ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )
        s2 = ms.create_staff_member(
            conn, 'jseinfeld', 'prettygood', ('Jerry', 'Seinfeld'),
            Permission.wait_staff
        )
        s3 = ms.create_staff_member(
            conn, 'gcostanza', 'prettygood', ('George', 'Costanza'),
            Permission.wait_staff
        )

        assert ms.lookup_id(conn, 'ldavid') == s1
        assert ms.lookup_id(conn, 'jseinfeld') == s2
        assert ms.lookup_id(conn, 'gcostanza') == s3


def test_get_missing_staff_member(db_connection):
    """Assert that a non-existing staff member is returned as None."""
    assert ms.get_staff_member(db_connection, 'ldavid') is None


def test_lookup_missing_member(database_snapshot):
    """Attempt to lookup id for missing member."""
    with database_snapshot.getconn() as conn:
        ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )

        assert ms.lookup_id(conn, 'spagetti') is None


def test_create_member_with_date(database_snapshot):
    """Create a staff member with a specific date."""
    start = datetime.datetime(
        2030, 9, 16, 0, 0,
        tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=3)  # Spice it up
    )
    with database_snapshot.getconn() as conn:
        ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff, start
        )

        member = ms.get_staff_member(conn, 'ldavid')
        assert member.start_dt == start


def test_verify_password(database_snapshot):
    """Verify that the supplied password is correct."""
    with database_snapshot.getconn() as conn:
        ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )
        assert ms.verify_password(conn, 'ldavid', 'prettygood')


def test_verify_password_no_user(db_connection):
    """Verify that false is returned for no user."""
    assert ms.verify_password(db_connection, 'ldavid', 'prettygood') is False


def test_bad_password(database_snapshot):
    """Verify that the supplied password is incorrect."""
    with database_snapshot.getconn() as conn:
        ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )
        assert not ms.verify_password(conn, 'ldavid', 'prettybad')


def test_unknown_user(database_snapshot):
    """Verify that the supplied password is incorrect."""
    with database_snapshot.getconn() as conn:
        ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )
        assert not ms.verify_password(conn, 'mr_bean', 'teddy69')


def test_list_members(database_snapshot):
    """Test to list all the staff members."""
    expected = [
        Staff(1, 'ldavid', 'prettygood', ('Larry', 'David'),
              'ignored', Permission.management),
        Staff(2, 'jseinfeld', 'idontwanttobeapriate', ('Jerry', 'Seinfeld'),
              'ignored', Permission.wait_staff),
        Staff(3, 'gcostanza', 'serenitynow', ('George', 'Costanza'),
              'ignored', Permission.robot)
    ]

    with database_snapshot.getconn() as conn:
        for staff in expected:
            ms.create_staff_member(
                conn, staff.username, staff.hashed_password,
                (staff.first_name, staff.last_name),
                staff.permission
            )

        actual = ms.list_members(conn)
        assert len(actual) == 3
        for i in range(0, 3):
            assert actual[i].username == expected[i].username
            assert sha256_crypt.verify(
                expected[i].hashed_password, actual[i].hashed_password
            )
            assert actual[i].first_name == expected[i].first_name
            assert actual[i].last_name == expected[i].last_name
            assert actual[i].permission == expected[i].permission
