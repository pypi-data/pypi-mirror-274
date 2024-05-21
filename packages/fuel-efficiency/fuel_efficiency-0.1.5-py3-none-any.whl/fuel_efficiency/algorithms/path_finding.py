from abc import ABC, abstractmethod
from typing import List, Tuple

from fuel_efficiency.entities.node import Node


class PathfindingStrategy(ABC):
    """
    Abstract Base Class used to implement a Path Finding algorithms.

    This class is the superclass of a Abstract Base Class (ABC) called ``PathfindingStrategy`` that provides abstract methods:
     find_path, get_neighbors, calculate_distance and calculate_fuel_consumption

    Those methods must be implemented in subclasses.

    """

    @abstractmethod
    def find_path(grid: List[List[Node]], start: Node, end: Node):
        """
        Abstract method to find the shortest path from start to end node in grid using PathfindingStrategy.
        It must be implemented in subclasses.

        Args:
            grid (List[List[Node]]): The grid used to find the shortest path.
            start (Node): The starting node.
            end (Node): The ending node.

        Returns:
            List[Node]: The shortest path.
        """
        pass   # pragma: no cover

    @abstractmethod
    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        """
        Abstrect methid to get a list with all the neighbors of the given node.
        It must be implemented in subclasses.

        Args:
            grid (List[List[Node]]): The grid used to find the neighbors.
            node (Node): The node.

        Returns:
            List[Node]: The neighbors of the given node.
        """
        pass   # pragma: no cover

    @abstractmethod
    def calculate_distance(node1: Node, node2: Node) -> float:
        """
        Abstract method to calculate the distance between two nodes as a heuristic to use on a PathfindingStrategy.
        It must be implemented in subclasses.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            float: The manhattan distance.
        """
        pass   # pragma: no cover

    @abstractmethod
    def calculate_fuel_consumption(
        grid: List[List[Node]], start: Node, end: Node
    ) -> Tuple[float, List[Node]]:
        """
        Abstract method to calculate the fuel consumption of a car that goes over the shortest path on a grid with different terrains to use
         on a PathfindingStrategy.
        It must be implemented in subclasses.

        Args:
            grid (List[List[Node]]): The grid used to find the fuel consumption.
            start (Node): The starting node.
            end (Node): The ending node.

        Returns:
            float: The fuel consumption.
            List[Node]: The shortest path.
        """
        pass   # pragma: no cover
