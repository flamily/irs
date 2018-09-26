import pytest
from irs.test.fixtures import db_connection

class TestSchema():
    def test_staff_present(self, db_connection):
        expected = {
            "jclank": True,
            'ckramer': True,
            'gcostanza': True,
        }
        with db_connection.cursor() as curs:
            curs.execute("SELECT username FROM staff")
            for staff in curs:
                print(staff)
                assert expected.pop(staff[0])
        assert len(expected) == 0