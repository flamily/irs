"""
Include test fixtures here for auto-discovery
These imports are used but for some reason pylint is not picking that up
so we'll just shush these for now until we figure out what's the go.
"""
# pylint: disable=unused-import
from test.fixtures.db_connection import db_connection  # noqa: F401
from test.fixtures.db_connection import database  # noqa: F401
from test.fixtures.db_connection import database_snapshot  # noqa: F401
from test.fixtures.flask_app import app  # noqa: F401
from test.fixtures.flask_app import client  # noqa: F401
