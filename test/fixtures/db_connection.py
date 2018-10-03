import os

import pytest
import psycopg2
import uuid

# Start of test:
# connect to box
# create new database with guid name
# apply schema
# add test values

# after tests:
# nuke that database


def schema_string():
    with open("db/schema.sql", 'r') as schema:
        for line in schema.readline():
            if line.startswith('-') or line.startswith('\n') or len(line) < 1:
                continue
            yield line
        # return schema.read()


def connection_string():  # pragma: no cover
    if os.environ.get("TRAVIS", False):
        return "user='postgres' host='localhost'"  # pragma: no cover
    return "user='postgres' host='localhost'"


@pytest.fixture(scope="session")
def database():
    identifier = uuid.uuid4().hex
    db_name = "irs_{}".format(identifier)
    schema_name = "irs_schema_{}".format(identifier)
    full_connection = "{} dbname={}".format(connection_string(), db_name)

    # create the database
    conn = psycopg2.connect(connection_string())
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute('CREATE DATABASE {};'.format(db_name))
    conn.close()

    # apply the schema
    conn = psycopg2.connect(full_connection)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute('CREATE SCHEMA {};'.format(schema_name))
        with open("db/schema.sql", 'r') as schema:
            cur.execute(schema.read())
    conn.close()

    # yield the connection string
    yield full_connection

    # cleanup
    # have to make a new connection to the 'postgres' (default) database
    #  as we are not allowed to drop the current database (irs_####).
    conn = psycopg2.connect(connection_string())
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute('DROP DATABASE {};'.format(db_name))
    conn.close()


@pytest.fixture()
def db_connection(database):
    # todo: connection pooling
    conn = psycopg2.connect(database)
    yield conn
    conn.rollback()
    conn.close()
