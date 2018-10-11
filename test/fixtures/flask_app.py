import pytest
from irs import app as web


@pytest.fixture
def app(database_snapshot):
    web.app.config['TESTING_DB_POOL'] = database_snapshot
    return web.app


@pytest.fixture
def client(app):
    # pylint:disable=redefined-outer-name
    return app.test_client()
