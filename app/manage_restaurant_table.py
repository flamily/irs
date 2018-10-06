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
        elif recent_event is (Event.seated or Event.attending):
            return State.occupied
        elif recent_event is (Event.maintaining or Event.paid):
            return State.unavailable
        else:
            raise Exception('Unknown event')


class RestaurantTable():
    """Object version of restaurant table db record."""

    def __init__(self, id, shape, coordinate, width, height, state, capacity):
        """Create a restaurant table."""
        self.id = id
        self.shape = Shape(str(shape))  # You can pass the enum, or a string!
        self.coordinate = None  # Coordinate(0, 0)
        self.state = State(str(state))
        self.capacity = capacity
        self.width = width
        self.height = height
