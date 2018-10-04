import os
from irs.db.connection import DatabaseConnectionPool

def inc(start):
    return start + 1


def test_answer():
    assert inc(3) == 4


def test_ass():
    assert inc(4) == 5


def example_db_conn_pool():
    conn_str = "dbname={} host={} user={}".format(
        "travis_ci_test" if os.environ.get("TRAVIS", True) else "irs",
        "localhost",
        "postgres"
    )

    pool = DatabaseConnectionPool(
        minconn=1, maxconn=20, connection_str=conn_str
    )

    with pool:
        with pool.get_connection() as conn:
            with conn.get_cursor() as cur:
                cur.execute("select username from staff")
                staff_usernames = cur.fetchall()
                assert ('jclank',) in staff_usernames
