import pytest
from irs import irs_app


@pytest.fixture
def app(database_snapshot):
    irs_app.app.config['TESTING_DB_POOL'] = database_snapshot
    print(dir(irs_app.app))

    yield irs_app.app


@pytest.fixture
def client(app):
    # pylint:disable=redefined-outer-name
    return app.test_client()
