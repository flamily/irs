import pytest
from irs.test.fixtures import db_connection

class TestSchema():
    def test_things(self, db_connection):
        with db_connection.cursor() as curs:
            curs.execute("SELECT * FROM staff")
            for staff in curs:
                print(staff)
        assert False