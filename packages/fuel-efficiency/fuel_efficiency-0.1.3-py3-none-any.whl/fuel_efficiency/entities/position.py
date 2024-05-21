import sys
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True, frozen=True)
class Position:
    """
    A class used to represent a Position (x,y)

    A ``Position(x,y)`` is a position on a grid with x axis and y axis.

    This class uses ``dataclasses`` that provides a decorator and functions for automatically adding generated special
    methods such as ``__init__()`` and ``__repr__()``

    Attributes:
        x (int): position value on x-axis
        y (int): position value on x-axis
    """

    x: int = sys.maxsize
    y: int = sys.maxsize

    def __add__(self, other: 'Position') -> Optional['Position']:
        """
        Add two Position objects together.

        Args:
            other (Position): The other Position object to add to this one.

        Returns:
            Position: The sum of the two Position objects.

        Raises:
            NotImplementedError: If the other argument is not a Position object.

        """
        try:
            return Position(self.x + other.x, self.y + other.y)
        except AttributeError:
            raise NotImplementedError(f'Cannot add Position and {type(other)}')

    def __sub__(self, other: 'Position') -> Optional['Position']:
        """
        Subtract two Position objects.

        Args:
            other (Position): The other Position object to subtract from this one.

        Returns:
            Position: The difference of the two Position objects.

        Raises:
            NotImplementedError: If the other argument is not a Position object.

        """
        try:
            return Position(self.x - other.x, self.y - other.y)
        except AttributeError:
            raise NotImplementedError(
                f'Cannot subtract Position and {type(other)}'
            )
