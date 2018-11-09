import os


def connection_string():  # pragma: no cover
    if os.environ.get("TRAVIS", False):
        return "user='postgres' host='localhost'"
    if os.environ.get("DATABASE_URL", False):
        return os.environ["DATABASE_URL"]
    return "user='postgres' host='localhost' dbname='irs'"


def is_running_on_lambda():
    root = os.environ.get("LAMBDA_TASK_ROOT", '')
    return len(root) > 0
