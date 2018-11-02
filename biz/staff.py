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


# pylint:disable=too-few-public-methods,too-many-arguments
class Staff():
    """Object version of the staff db record."""

    def __init__(self, s_id, username, hashed_password, full_name,
                 start_dt, permission):
        """Store a staff record.

        :param s_id: The staff member's unique db id.
        :param username: The staff member's unique username.
        :param hashed_password: A SHA256 representation of their password.
        :param full_name: A tuple containing (fist_name, last_name).
        :param start_dt: A datetime object specifying their starting date.
        :param permission: An instance of the Permission enum.
        """
        self.s_id = int(s_id)
        self.username = username
        self.hashed_password = hashed_password
        self.first_name = full_name[0]
        self.last_name = full_name[1]
        self.start_dt = start_dt  # A datetime object
        self.permission = Permission(str(permission))
    
    @staticmethod
    def minimum_username_length():
        return 3
    
    @staticmethod
    def minimum_password_length():
        return 10
