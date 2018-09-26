import pytest
from tests.fixtures.irs_db import db_connection

class TestSchema():
    def test_things(self, db_connection):
        print(db_connection)
        assert False