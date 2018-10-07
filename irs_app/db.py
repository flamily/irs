from flask import g, current_app
from psycopg2 import pool
import threading
from werkzeug.local import LocalProxy
from irs import config


__pool = None
__pool_lock = threading.Lock()


def __lazy_pool():
    """
    Unsure if the singleton needs to be thread safe
    Using double locking pattern to be sure.
    """
    global __pool
    if not __pool:
        with __pool_lock:
            if not __pool:
                __pool = pool.ThreadedConnectionPool(1, 5, config.connection_string())
    return __pool


def __pool_facade():
    """
    Allows unit tests to inject a connection pool
    Consider inverting this and putting it inside the singleton constructor '__lazy_pool'
    """
    injected_pool = current_app.config.get('TESTING_DB_POOL', None)
    if injected_pool is None:
        return __lazy_pool()
    return injected_pool


def register(app):
    app.teardown_appcontext(__teardown_db_conn)


def get_db_conn():
    if 'db_conn' not in g:
        g.db_conn = __pool_facade().getconn()
    return g.db_conn


db = LocalProxy(get_db_conn)


def __teardown_db_conn(exception=None):
    # if the request has an error,
    #  might need to close the connection and make a new one
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        if exception is not None:
            print('exception, rolling back transaction')
            db_conn.rollback()
        db_conn.commit()
        __pool_facade().putconn(db_conn)
