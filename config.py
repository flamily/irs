import os


def connection_string():  # pragma: no cover
    if os.environ.get("TRAVIS", False):
        return "user='postgres' host='localhost'"  # pragma: no cover
    return "user='postgres' host='localhost'"