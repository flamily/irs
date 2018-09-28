from db.connection import DatabaseConnectionPool, DatabaseConnection, DatabaseCursor


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


def test_database():

    with DatabaseConnectionPool("irs", "postgres", "postgres") as pool:
        with pool.get_connection() as conn:
            with conn.get_cursor() as cur:
                cur.execute("select username from staff")
                staff_usernames = cur.fetchall()
                assert ('jclank',) in staff_usernames
