from dataclasses import dataclass, field
from typing import Optional, Protocol

from fuel_efficiency.entities.position import Position


@dataclass(slots=True, eq=False)
class Node(Protocol):
    """
    A class used to represent a Node

    A Node contain a ``Position(x,y)`` that is a position on a grid and a ``weight`` that represents the weight for a
    vehicle to move through different terrains, that affects its fuel efficiency.

    This class uses ``dataclasses`` that provides a decorator and functions for automatically adding generated special
    methods such as ``__init__()`` and ``__repr__()``

    Attributes:
        weight (float): position value on x-axis
        position (Position): position value on x-axis
    """

    weight: float
    position: Position = field(default_factory=Position)

    def __eq__(self, other: 'Position') -> Optional[bool]:
        """
        Compare two Nodes objects.

        Args:
            other (Node): The other Node object to compare with this one.

        Returns:
            bool: True if the other Node is equal to the current one False otherwise.

        Raises:
            NotImplementedError: If the other argument is not a Position object.
        """
        try:
            return (self.position == other.position) and (
                self.weight == other.weight
            )
        except AttributeError:
            raise NotImplementedError(
                'Missing `position` or `weight` attribute'
            )

    def __lt__(self, other: 'Position') -> Optional[bool]:
        """
        Compare the weights of two Nodes objects.

        Args:
            other (Node): The other Node object to compare with this one.

        Returns:
            bool: True if the other Node has a greater weight than the current one False otherwise.

        Raises:
            NotImplementedError: If the other argument is not a Position object.
        """
        try:
            return self.weight < other.weight
        except AttributeError:
            raise NotImplementedError('Missing `weight` attribute')
