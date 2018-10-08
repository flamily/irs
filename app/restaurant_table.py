"""
Classes defining a restaurant table.

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
        return self.value  # pragma: no cover

    @staticmethod
    def resolve_state(latest_event):
        """Resolve a state based on the most recent event."""
        parsed = Event(str(latest_event))  # Make sure it's actually an event

        if parsed in [Event.seated, Event.attending]:
            return State.occupied
        if parsed in [Event.maintaining, Event.paid]:
            return State.unavailable
        return State.available


# pylint:disable=too-few-public-methods,too-many-arguments
class RestaurantTable():
    """Object version of restaurant table db record."""

    def __init__(self, rt_id, shape, coordinate, width, height,
                 latest_event, capacity):
        """Create a restaurant table."""
        self.rt_id = int(rt_id)
        self.shape = Shape(str(shape))  # You can pass the enum, or a string!
        self.coordinate = coordinate    # Expects the named tuple 'Coordinate'
        self.latest_event = Event(str(latest_event))
        self.capacity = int(capacity)
        self.width = int(width)
        self.height = int(height)

    @property
    def state(self):
        """Determine the state of the table based on the most recent event."""
        return State.resolve_state(self.latest_event)
