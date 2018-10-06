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
        return self.value


class Event(Enum):
    """An enum that specifies the events that occur at a restaurant table."""

    ready = 'ready'
    seated = 'seated'
    attending = 'attending'
    paid = 'paid'
    maintaining = 'maintaining'

    def __str__(self):
        """Return string version of enum."""
        return self.value


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
        if recent_event is Event.ready:
            return State.available
        elif recent_event in [Event.seated, Event.attending]:
            return State.occupied
        elif recent_event in [Event.maintaining, Event.paid]:
            return State.unavailable
        else:
            raise Exception('Unknown event: {}'.format(recent_event))


class RestaurantTable():
    """Object version of restaurant table db record."""

    def __init__(self, id, shape, coordinate, width, height, state, capacity):
        """Create a restaurant table."""
        self.id = int(id)
        self.shape = Shape(str(shape))  # You can pass the enum, or a string!
        self.coordinate = coordinate  # Expects a coordinate named tuple
        self.state = State(str(state))
        self.capacity = int(capacity)
        self.width = int(width)
        self.height = int(height)


class ManageRestaurantTable():
    """Class for managing restaurant tables."""

    def __init__(self, db_connection):
        """
        Initialise the manager.

        :param db_connection: A psycopg2 connection to the database.
        """
        self.db_connection = db_connection

    def list(self):
        """List of all the restaurant tables.

        :return: Return a list of restaurant tables, and a template id.
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
            for rt in curs.fetchall():
                rt_list.append(
                    RestaurantTable(
                        id=rt[0],
                        capacity=rt[1],
                        coordinate=Coordinate(x=rt[2], y=rt[3]),
                        width=rt[4],
                        height=rt[5],
                        shape=Shape(rt[6]),
                        state=State.resolve_state(Event(rt[7]))
                    )
                )

            return rt_list
