import os

import pytest
import psycopg2

# Start of test:
# connect to box
# create new database with guid name
# apply schema
# add test values

# after tests:
# nuke that database

def connection_string(): #pragma: no cover
    if os.environ.get("TRAVIS", False):
        return "user='postgres' host='localhost'" #pragma: no cover
    return "user='postgres' host='localhost' password='mysecretpassword'"

@pytest.fixture()
def db_connection():
    conn = psycopg2.connect(connection_string()) # this might blow up, but that is ok in tests.
    yield conn
