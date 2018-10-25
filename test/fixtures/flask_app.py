import pytest
import web


@pytest.fixture
def app(database_snapshot):
    web.APP.config['TESTING_DB_POOL'] = database_snapshot
    web.APP.testing_db_pool = database_snapshot
    return web.APP


@pytest.fixture
def client(app):
    # pylint:disable=redefined-outer-name
    client = app.test_client()
    client.testing_db_pool = app.testing_db_pool
    return client
