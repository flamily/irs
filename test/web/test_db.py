from irs.web.db import db


def test_db_commit(app):
    def add_staff():
        with db.cursor() as curs:
            curs.execute(
                "INSERT INTO staff "
                "(username, password, first_name, last_name, permission) "
                "values (%s, %s, %s, %s, %s)",
                (
                    'george',
                    'password',
                    'george',
                    'george',
                    'management'
                )
            )
        return "success"
    app.add_url_rule('/add_staff', 'add_staff', add_staff)
    client = app.test_client()

    client.get('/add_staff')

    pool = app.config['TESTING_DB_POOL']
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM staff")
            assert curs.rowcount is 1
    finally:
        pool.putconn(conn)


def test_db_rollback(app):
    def throw_wobbly():
        with db.cursor() as curs:
            curs.execute(
                "INSERT INTO staff "
                "(username, password, first_name, last_name, permission) "
                "values (%s, %s, %s, %s, %s)",
                (
                    'george',
                    'password',
                    'george',
                    'george',
                    'management'
                )
            )
        raise ValueError('we wanted this to happen')
    app.add_url_rule('/throw_wobbly', 'throw_wobbly', throw_wobbly)
    client = app.test_client()

    client.get('/throw_wobbly')

    pool = app.config['TESTING_DB_POOL']
    conn = pool.getconn()
    try:
        with conn.cursor() as curs:
            curs.execute("SELECT * FROM staff")
            assert curs.rowcount is 0
    finally:
        pool.putconn(conn)
