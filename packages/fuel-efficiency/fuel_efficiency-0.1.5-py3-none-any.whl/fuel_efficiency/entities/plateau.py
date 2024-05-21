from dataclasses import dataclass, field

from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.position import Position


@dataclass(slots=True, eq=False, unsafe_hash=True)
class Plateau(Node):
    """
    A class used to represent a plateau terrain (Node)

    A plateau terrain is a Node that inherits the following attributes a ``Position(x,y)`` that is a position on a
    grid and a ``weight`` that represents the weight for a vehicle to move through different terrains, that affects its
    fuel efficiency. in this case the default weight is 1.

    This class uses ``dataclasses`` that provides a decorator and functions for automatically adding generated special
    methods such as ``__init__()`` and ``__repr__()``

    Attributes:
        weight (float): position value on x-axis
        position (Position): position value on x-axis
    """

    weight: float = float(1)
    position: Position = field(default_factory=Position)
