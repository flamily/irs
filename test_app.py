import os
from irs.db.connection import DatabaseConnectionPool

def inc(start):
    return start + 1


def test_answer():
    assert inc(3) == 4


def test_ass():
    assert inc(4) == 5
