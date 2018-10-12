import pytest
from irs import web


@pytest.fixture
def app(database_snapshot):
    web.APP.config['TESTING_DB_POOL'] = database_snapshot
    return web.APP


@pytest.fixture
def client(app):
    # pylint:disable=redefined-outer-name
    return app.test_client()
