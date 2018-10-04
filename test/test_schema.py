import pytest
import psycopg2


def test_staff_empty(db_cursor):
    # with db_connection.cursor() as curs:
    db_cursor.execute("SELECT username FROM staff")
    assert db_cursor.rowcount is 0


def test_non_existant_table(db_cursor):
    with pytest.raises(psycopg2.ProgrammingError):
        db_cursor.execute("SELECT username FROM wew_lad")


def test_insert_staff(db_cursor):
    db_cursor.execute(
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

    db_cursor.execute("SELECT username FROM staff")
    for staff in db_cursor:
        print(staff)
        assert expected.pop(staff[0])

    assert not expected
