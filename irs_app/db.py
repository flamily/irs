from flask import current_app, g
from flask.cli import with_appcontext

from psycopg2 import pool
from irs import config
from werkzeug.local import LocalProxy

__pool = pool.ThreadedConnectionPool(1, 5, config.connection_string())


def register(app):
    app.teardown_appcontext(__teardown_db_conn)


def get_db_conn():
    if 'db_conn' not in g:
        g.db_conn = __pool.getconn()
    return g.db_conn


db = LocalProxy(get_db_conn)


def __teardown_db_conn(exception=None):
    #if the request has an error, close the connection and make a new one
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        if exception is not None:
            print('exception, rolling back transaction')
            db_conn.rollback()
        db_conn.commit()
        __pool.putconn(db_conn)