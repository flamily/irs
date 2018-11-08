"""
Driver for managing staff records in the database.

This file contains a series of functions that manipulate and access records
in the datbase pertaining to management of staff and authentication.

Author: Andrew Pope
Date: 09/10/2018
"""
from passlib.hash import sha256_crypt
from irs.app.src.staff import Staff


def lookup_id(db_conn, username):
    """Get a staff member's unique id used in restaurant events.

    :param db_conn: A psycopg2 connection to the database.
    :param username: The username of the staff member.
    :return: staff_id.
    :note: Will throw exception if staff member does not exist.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT staff_id FROM staff WHERE username = %s", (username,)
        )
        s_id = curs.fetchone()[0]
    return s_id


def verify_password(db_conn, username, password):
    """Verify that the supplied staff password is correct.

    :param db_conn: A psycopg2 connection to the database.
    :param username: The username of the staff member.
    :param password: The password to verify against the database.
    :return: True if the user exists and the password is correct.
    :note: Will throw exception if staff member does not exist.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT password FROM staff WHERE username = %s",
            (username,)
        )
        pwhash = curs.fetchone()[0]
    return sha256_crypt.verify(password, pwhash)


def get_staff_member(db_conn, username):
    """Get the member based on their username.

    :param db_conn: A psycopg2 connection to the database.
    :param username: The username of the staff member.
    :return: A Staff object.
    :note: Will throw exception if staff member does not exist.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT * FROM staff WHERE username = %s", (username,)
        )
        member = curs.fetchone()
        return Staff(
            s_id=member[0],
            username=member[1],
            hashed_password=member[2],
            full_name=(member[3], member[4]),
            start_dt=member[5],
            permission=member[6]
        )


def list_members(db_conn):
    """Get a list of all staff members in the database.

    :param db_conn: A psycopg2 connection to the database.
    :return: A list of Staff objects.
    """
    with db_conn.cursor() as curs:
        curs.execute(
            "SELECT * FROM staff"
        )
        staff_members = []
        for member in curs.fetchall():
            staff_members.append(
                Staff(
                    s_id=member[0],
                    username=member[1],
                    hashed_password=member[2],
                    full_name=(member[3], member[4]),
                    start_dt=member[5],
                    permission=member[6]
                )
            )

    return staff_members


# pylint:disable=too-many-arguments
def create_staff_member(db_conn, username, password,
                        full_name, permission, start_dt=None):
    """Insert a staff member into the database.

    :param db_conn: A psycopg2 connection to the database.
    :param username: A unique username that the member will use to login.
    :param password: Their password (in cleartext) for them to login.
    :param full_name: A tuple of the member's (first_name, last_name.
    :param permission: An instance of the Permission enum.
    :param start_dt: If not None, this must be a python datetime object.
    Otherwise, the current datetime will be used (on the db side).
    :return: Id of the newly created staff member.
    """
    pwhash = sha256_crypt.hash(password)  # Hash the password with sha256 first
    with db_conn.cursor() as curs:
        if start_dt is None:
            curs.execute(
                "INSERT INTO staff "
                "(username, password, first_name, last_name, permission) "
                "VALUES (%s, %s, %s, %s, %s) "
                "RETURNING staff_id",
                (
                    username, pwhash, full_name[0], full_name[1],
                    str(permission)
                )
            )
        else:
            curs.execute(
                "INSERT INTO staff "
                "(username, password, first_name, last_name, permission, "
                "start_dt) "
                "VALUES (%s, %s, %s, %s, %s, %s) "
                "RETURNING staff_id",
                (
                    username, pwhash, full_name[0], full_name[1],
                    str(permission), str(start_dt)
                )
            )

        s_id = curs.fetchone()[0]
    return s_id
