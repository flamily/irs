"""
An interface for managing the restaurant table records in the database.

Author: Andrew Pope
Date: 06/10/2018
"""
import collections
from enum import Enum

Coordinate = collections.namedtuple('Coordinate', 'x y')


class Shape(Enum):
    """An enum that specifies the various shapes of a restaurant table."""

    rectangle = 'rectangle'
    ellipse = 'ellipse'

    def __str__(self):
        """Return string version of enum."""
        return self.value  # pragma: no cover


class Event(Enum):
    """An enum that specifies the events that occur at a restaurant table."""

    ready = 'ready'
    seated = 'seated'
    attending = 'attending'
    paid = 'paid'
    maintaining = 'maintaining'

    def __str__(self):
        """Return string version of enum."""
        return self.value  # pragma: no cover


class State(Enum):
    """An enum that specifies the various states of a restaurant table."""

    available = 'available'
    unavailable = 'unavailable'
    occupied = 'occupied'

    def __str__(self):
        """Return string version of enum."""
        return self.value

    @staticmethod
    def resolve_state(recent_event):
        """Resolve a state based on the most recent event."""
        parsed = Event(str(recent_event))  # Make sure it's actually an event

        if parsed in [Event.seated, Event.attending]:
            return State.occupied
        elif parsed in [Event.maintaining, Event.paid]:
            return State.unavailable
        else:
            return State.available


class RestaurantTable():  # pylint:disable=too-few-public-methods
    """Object version of restaurant table db record."""

    def __init__(self, rt_id, shape, coordinate, width, height,
                 state, capacity):
        """Create a restaurant table."""
        self.rt_id = int(rt_id)
        self.shape = Shape(str(shape))  # You can pass the enum, or a string!
        self.coordinate = coordinate  # Expects a coordinate named tuple
        self.state = State(str(state))
        self.capacity = int(capacity)
        self.width = int(width)
        self.height = int(height)


class ManageRestaurantTable():  # pylint:disable=too-few-public-methods
    """Class for managing restaurant tables."""

    def __init__(self, db_connection):
        """
        Initialise the manager.

        :param db_connection: A psycopg2 connection to the database.
        """
        self.db_connection = db_connection

    def ready(self):
        assert True

    def maintain(self):
        assert True

    def ordered(self):
        """Menu items etc??"""
        assert True

    def paid(self, table_id, staff_id):
        """...."""
        # with self.db_connection.cursor() as curs:
        # db_cursor.execute(
        #     "INSERT INTO event "
        #     "(description, restaurant_table_id, staff_id) "
        #     "VALUES (%s, %s, %s) "
        #     "RETURNING event_id",
        #     (
        #         description, restaurant_table_id, staff_id
        #     )
        # )
        assert True

    def applyConfirmation(self, table_id, staff_id, party_size):
        """...."""
        # Inserts reservation, event??
        assert True

    def list(self):
        """List of all the restaurant tables.

        :return: Return a list of restaurant tables.
        """
        with self.db_connection.cursor() as curs:
            curs.execute(
                "SELECT rt.*, et.description "
                "FROM restaurant_table rt "
                "JOIN event et on et.restaurant_table_id=rt.restaurant_table_id "  # noqa: E501
                "WHERE et.event_id = ("
                " SELECT e.event_id FROM event e "
                " WHERE e.restaurant_table_id = rt.restaurant_table_id "
                " ORDER BY event_dt desc LIMIT 1"
                ")"
            )

            rt_list = []
            for table in curs.fetchall():
                rt_list.append(
                    RestaurantTable(
                        rt_id=table[0],
                        capacity=table[1],
                        coordinate=Coordinate(x=table[2], y=table[3]),
                        width=table[4],
                        height=table[5],
                        shape=Shape(table[6]),
                        state=State.resolve_state(Event(table[7]))
                    )
                )

            return rt_list
