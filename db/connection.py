"""
A collection of classes used to access the database in a controlled manner.

Author: Andrew Pope
Date: 28/09/2018
"""
from psycopg2.pool import ThreadedConnectionPool


class DatabaseConnectionPool:
    """Create a threaded connection pool for a PostgreSQL database."""

    def __init__(self, connection_str, minconn=1, maxconn=20):
        """Establish connection with the database and create the pool."""
        self.minconn = minconn
        self.maxconn = maxconn
        self.connection_str = connection_str
        self.__pool = None

    def get_connection(self):
        """Get a connection from the pool."""
        if self.__pool is None:
            # Make sure callers use the `with` pattern for automatic context
            # management
            raise Exception(
                "A connection can only be obtained within a context manager."
            )

        return DatabaseConnection(self.__pool)

    def __enter__(self):
        """Return a database connection pool object."""
        # Establish a connection pool to the database
        self.__pool = ThreadedConnectionPool(
            self.minconn,
            self.maxconn,
            self.connection_str
        )  # REVIEW: Do we care about allowing this object ot be threaded?

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection pool."""
        if self.__pool:
            self.__pool.closeall()
            self.__pool = None


class DatabaseConnection:
    """Establish a connection to a PostgreSQL database."""

    def __init__(self, pool):
        """Pull a connection from the pool and store."""
        self.__pool = pool  # The connection needs to know from whence it came
        self.__connection = None

    def get_cursor(self):
        """Get a cursor from the database connection."""
        if self.__connection is None:
            # Make sure callers use the `with` pattern for automatic context
            # management
            raise Exception(
                "A cursor can only be obtained within a context manager."
            )

        return DatabaseCursor(self.__connection)

    def rollback(self):
        """Rollback any commits that may have happend in the transaction."""
        if self.__connection is None:
            raise Exception(
                "A connection must occur within a context manager."
            )

        self.__connection.rollback()

    def __enter__(self):
        """Return a connection from the pool."""
        self.__connection = self.__pool.getconn()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Return a connection to the pool."""
        if self.__connection:
            self.__pool.putconn(self.__connection)
            self.__connection = None


class DatabaseCursor:
    """Create a cursor for database queries."""

    def __init__(self, connection):
        """Create a cursor from the connection."""
        self.__connection = connection
        self.__cursor = None

    def __enter__(self):
        """Return a psycopg2 cursor for use."""
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the cursor."""
        if self.__cursor:
            self.__cursor.close()
            self.__cursor = None
