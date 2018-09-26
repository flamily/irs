import pytest

@pytest.fixture()
def db_connection():
    print('bingo')
    yield "wew"
    print('bongo')