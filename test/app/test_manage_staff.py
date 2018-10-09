"""
These tests check the staff manager.

Author: Andrew Pope
Date: 09/10/2018
"""
import pytest
import psycopg2
import datetime
from datetime import tzinfo
import irs.app.manage_staff as ms
from irs.app.staff import (Staff, Permission)
from passlib.hash import sha256_crypt

"""
Tests:
- list
- lookup
- Create with a different start date (datetime)
"""



def test_create_member(database_snapshot):
    """Create a staff member."""
    with database_snapshot.getconn() as conn:
        s_id = ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )

        member = ms.get_member(conn, 'ldavid')
        assert member.s_id == s_id
        assert member.permission == Permission.wait_staff
        assert member.first_name == 'Larry'
        assert member.last_name == 'David'
        assert member.hashed_password != 'prettygood'
        assert sha256_crypt.verify('prettygood', member.hashed_password)


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

        member = ms.get_member(conn, 'ldavid')
        assert member.start_dt == start


def test_verify_password(database_snapshot):
    """Verify that the supplied password is correct."""
    with database_snapshot.getconn() as conn:
        ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )
        assert ms.verify_password(conn, 'ldavid', 'prettygood')


def test_bad_password(database_snapshot):
    """Verify that the supplied password is incorrect."""
    with database_snapshot.getconn() as conn:
        ms.create_staff_member(
            conn, 'ldavid', 'prettygood', ('Larry', 'David'),
            Permission.wait_staff
        )
        assert not ms.verify_password(conn, 'ldavid', 'prettybad')


class Staff():
    """Object version of the staff db record."""

    def __init__(self, s_id, username, hashed_password, first_name, last_name,
                 start_dt, permission):
        """Store a staff record."""
        self.s_id = int(s_id)
        self.username = username
        self.hashed_password = hashed_password
        self.first_name = first_name
        self.last_name = last_name
        self.start_dt = start_dt  # A datetime object
        self.permission = Permission(str(permission))


def test_list_members(database_snapshot):
    """Test to list all the staff members."""
    expected = [
        Staff(1, 'ldavid', 'prettygood', 'Larry', 'David',
              'ignored', Permission.management),
        Staff(2, 'jseinfeld', 'idontwanttobeapriate', 'Jerry', 'Seinfeld',
              'ignored', Permission.wait_staff),
        Staff(3, 'gcostanza', 'serenitynow', 'George', 'Costanza',
              'ignored', Permission.robot)
    ]

    with database_snapshot.getconn() as conn:
        for staff in expected:
            ms.create_staff_member(
                conn, staff.username, staff.hashed_password,
                (staff.first_name, staff.last_name),
                staff.permission
            )

        actual = ms.list(conn)
        assert len(actual) == 3
        for i in range(0, 3):
            assert actual[i].username == expected[i].username
            assert sha256_crypt.verify(
                expected[i].hashed_password, actual[i].hashed_password
            )
            assert actual[i].first_name == expected[i].first_name
            assert actual[i].last_name == expected[i].last_name
            assert actual[i].permission == expected[i].permission
