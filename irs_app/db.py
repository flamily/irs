from flask import current_app, g
from flask.cli import with_appcontext

from psycopg2 import pool
from irs import config


def register(app):
    app.teardown_request(__teardown_db_conn)
    app.teardown_appcontext(__teardown_db_pool)


def get_db_pool():
    if 'db_pool' not in g:
        g.db = pool.SimpleConnectionPool(1, 5, config.connection_string())
    return g.db


def get_db_conn():
    if 'db_conn' not in g:
        g.db_conn = get_db_pool().getconn()
    return g.db_conn


def __teardown_db_conn(exception=None):
    #if the request has an error, close the connection and make a new one
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        if exception is not None:
            db_conn.rollback()
        get_db_pool().putconn(db_conn)


# called when the app is shutting down
def __teardown_db_pool():
    print("close all the db connections")
    db = g.pop('db', None)
    if db is not None:
        db.closeall()