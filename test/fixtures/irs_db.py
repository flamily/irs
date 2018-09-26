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

def connection_string():
    if os.environ.get("TRAVIS", False):
        return "user='postgres' host='localhost'"
    return "user='postgres' host='localhost' password='mysecretpassword'"

@pytest.fixture()
def db_connection():
    try:
        conn = psycopg2.connect(connection_string())
        yield conn
    except:
        print("unable to connect to the database")