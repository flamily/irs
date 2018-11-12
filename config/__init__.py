import os


def connection_string():  # pragma: no cover
    if os.environ.get("TRAVIS", False):
        return "user='postgres' host='localhost'"
    if os.environ.get("DATABASE_URL", False):
        return os.environ["DATABASE_URL"]
    return "user='postgres' host='localhost'"


def is_running_on_lambda():
    root = os.environ.get("LAMBDA_TASK_ROOT", '')
    return len(root) > 0


def cf_api_key():  # pragma: no cover
    return os.environ.get("CF_API_KEY", 'fcef05be3b9f440f9e38dfb675b07de6')


def model_bucket():  # pragma: no cover
    return os.environ.get("MODEL_S3_BUCKET", 'irs-zappa')


def model_key():  # pragma: no cover
    return os.environ.get("MODEL_S3_KEY", 'RF_model.pkl')
