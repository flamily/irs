import pytest
import psycopg2
import os

# Start of test:
# connect to box
# create new database with guid name
# apply schema
# add test values

# after tests:
# nuke that database

def connection_string(): #pragma: no cover
    if os.environ.get("TRAVIS", False):
        return "user='postgres' host='localhost'"
    return "user='postgres' host='localhost' password='mysecretpassword'"

def wrap_exception():
    try:
        return psycopg2.connect(connection_string())
    except: #pragma: no cover
        print("unable to connect to the database")

@pytest.fixture()
def db_connection():
    conn = wrap_exception()
    yield conn