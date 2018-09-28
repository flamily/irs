"""
A collection of classes used to access the database in a controlled manner.

Author: Andrew Pope
Date: 28/09/2018
"""
import psycopg2


class DatabaseConnectionPool:
    """
    TODO: Should be a singleton (one pool only).

    Inherits from psycopg2? Takes database information as input.
    """

    __pool = None
    # getconn(): DatabaseConnection
    # putconn(DatabaseConnection):

    def __init__(self, database, user, password, host="127.0.0.1", port=5432, minconn=1, maxconn=20):
        """Establish connection with the database and create the pool."""
        self.__pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )  # REVIEW: Not sure if using Threaded over SimpleConnectionPool
        # has any implications.

    def __enter__(self):
        """Create a database connection pool."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection pool."""
        if (self.__pool):
            self.__pool.closeall()


class DatabaseConnection:
    """
    TODO: Can have many instances of DatabaseConnection.

    When used up, connection must be returned to pool.
    """
    # __enter__(): DatabaseCursor
    # __exit__():


class DatabaseCursor:
    """
    Not sure if actually required. We could return a psycopg2 cursor.

    However, not sure if we want to simplify the class....
    """
    # execute, fetchone, scroll -> all methods of psycopg2
