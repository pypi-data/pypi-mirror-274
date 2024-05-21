from dataclasses import dataclass, field
from typing import List

from fuel_efficiency.algorithms.dijkstra import DijkstraStrategy
from fuel_efficiency.algorithms.path_finding import PathfindingStrategy
from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.valley import Valley


@dataclass(slots=True)
class Context:
    """
    This is a Context class that uses the `@property` decorator in order to protect and define getters and setters.

    Attributes:
        _strategy (PathfindingStrategy): A PathfindingStrategy that can be (DijkstraStrategy, PathfindingStrategy)
        _grid (List[List[Node]): A 2D Grid that can have many nodes.
        _start Node: The starting node.
        _end Node: The ending node.

    """

    _strategy: PathfindingStrategy = field(default_factory=DijkstraStrategy)
    _grid: List[List[Node]] = field(
        default_factory=lambda: [
            [Valley() for _ in range(3)] for _ in range(3)
        ]
    )
    _start: Node = field(default_factory=Valley)
    _end: Node = field(default_factory=Valley)

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, new_grid: List[List[Node]]):
        """
        Setter for the grid property.

        Args:
            self._grid (List[List[Node]]): A 2D Grid.
            new_grid (List[List[Node]]): A new value for 2D Grid.

        Returns:
            None
        """
        if not isinstance(new_grid, list):
            raise TypeError('Grid must be a list')
        if not all(isinstance(row, list) for row in new_grid):
            raise TypeError('Grid must be a list of lists')
        self._grid = new_grid

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, new_start: Node):
        """
        Setter for the start property.

        Args:
            self._start (Node): The starting node.
            new_start (Node): The new value for starting node.

        Returns:
            None
        """
        self._start = new_start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, new_end: Node):
        """
        Setter for the end property.

        Args:
            self._end (Node): The ending node.
            new_end (Node): The new value for ending node.

        Returns:
            None
        """

        self._end = new_end

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, new_strategy: PathfindingStrategy):
        """
        Setter for the strategy property.

        Args:
            self._strategy: A PathfindingStrategy object.
            new_strategy: A new value for a PathfindingStrategy object.

        Returns:
            None
        """
        if not isinstance(new_strategy, PathfindingStrategy):
            raise TypeError(
                'Strategy must be an instance of PathfindingStrategy'
            )
        self._strategy = new_strategy

    def run(self):
        if not hasattr(self._strategy, 'find_path'):
            raise NotImplementedError(
                'Strategy must implement the find_path method'
            )
        return self._strategy.find_path(self.grid, self.start, self.end)
