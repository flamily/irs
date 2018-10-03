def test_staff_empty(db_connection):
    with db_connection.cursor() as curs:
        curs.execute("SELECT username FROM staff")
        assert curs.rowcount is 0


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
