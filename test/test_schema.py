import pytest
import psycopg2


def test_staff_empty(db_connection):
    with db_connection.cursor() as curs:
        curs.execute("SELECT username FROM staff")
        assert curs.rowcount is 0


def test_non_existant_table(db_connection):
    with db_connection.cursor() as curs:
        with pytest.raises(psycopg2.ProgrammingError):
            curs.execute("SELECT username FROM wew_lad")


def test_insert_staff(db_connection):
    with db_connection.cursor() as curs:
        curs.execute(
            "INSERT INTO staff "
            "(username, password, first_name, last_name, permission) "
            "values (%s, %s, %s, %s, %s)",
            (
                'gcostanza',
                'password',
                'george',
                'Costanza',
                'management'
            )
        )
    expected = {
        'gcostanza': True,
    }
    with db_connection.cursor() as curs:
        curs.execute("SELECT username FROM staff")
        for staff in curs:
            print(staff)
            assert expected.pop(staff[0])
    assert not expected
