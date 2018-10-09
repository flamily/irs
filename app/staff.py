"""
Classes defining a staff member.

Author: Andrew Pope
Date: 09/10/2018
"""
from enum import Enum


class Permission(Enum):
    """An enum that specifies the various permissions of a staff member."""

    robot = 'robot'
    wait_staff = 'wait_staff'
    management = 'management'

    def __str__(self):
        """Return string version of enum."""
        return self.value  # pragma: no cover


# pylint:disable=too-few-public-methods
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
        self.start_dt = start_dt
        self.permission = Permission(str(permission))
