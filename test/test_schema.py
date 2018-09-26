def test_staff_present(db_connection):
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
    assert not expected
