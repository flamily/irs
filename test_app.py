import os
from db.connection import DatabaseConnectionPool


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


def test_database():
    pool = None
    if 'TRAVIS' in os.environ:
        pool = DatabaseConnectionPool("travis_ci_test", "postgres")
    else:
        # TODO: This information for a developers local database
        # would be read from some file.
        pool = DatabaseConnectionPool("irs", "postgres", "postgres")

    with pool:
        with pool.get_connection() as conn:
            with conn.get_cursor() as cur:
                cur.execute("select username from staff")
                staff_usernames = cur.fetchall()
                assert ('jclank',) in staff_usernames
