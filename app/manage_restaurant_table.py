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


class State(Enum):
    """An enum that specifies the various states of a restaurant table."""

    available = 'available'
    unavailable = 'unavailable'
    occupied = 'occupied'

    def __str__(self):
        """Return string version of enum."""
        return self.value



class RestaurantTable():
    """Object version of restaurant table db record."""

    def __init__(self, shape, coordinate, state, capacity):
        """Create a restaurant table."""
        self.shape = Shape(shape)
        self.coordinate = None  # Coordinate(0, 0)
        self.state = None
        self.capacity = None
