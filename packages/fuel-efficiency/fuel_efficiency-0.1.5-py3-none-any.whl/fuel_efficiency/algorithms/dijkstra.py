import heapq
import math
from typing import List, Tuple

from fuel_efficiency.algorithms.path_finding import PathfindingStrategy
from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.position import Position


class DijkstraStrategy(PathfindingStrategy):
    """
    A class used to implement a simple Dijkstra algorithm that accept only horizontal and vertical directions.

    This class is a subclass of a Abstract Base Class (ABC) called ``PathfindingStrategy`` that provides abstract methods:
     find_path, get_neighbors, calculate_distance and calculate_fuel_consumption

    """

    cardinal_directions = [
        Position(-1, -1),
        Position(-1, 0),
        Position(-1, 1),
        Position(0, -1),
        Position(0, 1),
        Position(1, -1),
        Position(1, 0),
        Position(1, 1),
    ]

    def find_path(grid: List[List[Node]], start: Node, end: Node):
        """
        Find the shortest path from start to end node in grid using Dijkstra algorithm.

        Args:
            grid (List[List[Node]]): The grid used to find the shortest path.
            start (Node): The starting node.
            end (Node): The ending node.

        Returns:
            List[Node]: The shortest path.
        """
        rows, cols = len(grid), len(grid[0])
        distances = [[float('inf')] * cols for _ in range(rows)]
        distances[start.position.x][start.position.y] = grid[start.position.x][
            start.position.y
        ].weight

        previous = [[None] * cols for _ in range(rows)]

        pq = [(grid[start.position.x][start.position.y].weight, start)]

        if start != end:
            while pq:
                current_distance, current_node = heapq.heappop(pq)
                if current_node == end:
                    path = []
                    while current_node is not start:
                        path.append(current_node)
                        current_node = previous[current_node.position.x][
                            current_node.position.y
                        ]
                    return path[::-1]  # reversed path

                for neighbor in DijkstraStrategy.get_neighbors(
                    grid, current_node
                ):
                    new_distance = current_distance + (
                        neighbor.weight
                        * DijkstraStrategy.calculate_distance(
                            current_node, neighbor
                        )
                    )

                    if (
                        new_distance
                        < distances[neighbor.position.x][neighbor.position.y]
                    ):
                        distances[neighbor.position.x][
                            neighbor.position.y
                        ] = new_distance
                        previous[neighbor.position.x][
                            neighbor.position.y
                        ] = current_node
                        heapq.heappush(pq, (new_distance, neighbor))

        return []

    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        """
        Get a list with all the neighbors of the given node that are in any diagonal, horizontal and vertical direction.

        Args:
            grid (List[List[Node]]): The grid used to find the neighbors.
            node (Node): The node.

        Returns:
            List[Node]: The neighbors of the given node.
        """
        neighbors_list = []
        grid_xlen = len(grid)
        grid_ylen = len(grid[0])
        for direction in DijkstraStrategy.cardinal_directions:
            if (
                ((node.position.x + direction.x) >= 0)
                and ((node.position.y + direction.y) >= 0)
            ) and (
                ((node.position.x + direction.x) < grid_xlen)
                and ((node.position.y + direction.y) < grid_ylen)
            ):
                neighbors_list.append(
                    grid[node.position.x + direction.x][
                        node.position.y + direction.y
                    ]
                )

        return neighbors_list

    def calculate_distance(node1: Node, node2: Node) -> float:
        """
        Calculate the euclidian distance between two nodes as a heuristic to use on a Dijkstra algorithm.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            float: The manhattan distance.
        """
        return math.sqrt(
            (node2.position.x - node1.position.x) ** 2
            + (node2.position.y - node1.position.y) ** 2
        )

    def calculate_fuel_consumption(
        grid: List[List[Node]], start: Node, end: Node
    ) -> Tuple[float, List[Node]]:
        """
        Calculate the fuel consumption of a car that goes over the shortest path on a grid with different terrains using
         Dijkstra's algorithm.

        Args:
            grid (List[List[Node]]): The grid used to find the fuel consumption.
            start (Node): The starting node.
            end (Node): The ending node.

        Returns:
            float: The fuel consumption.
            List[Node]: The shortest path.
        """
        path = DijkstraStrategy.find_path(grid, start, end)
        fuel_consumption = 0
        for node in path:
            fuel_consumption += node.weight
        return fuel_consumption, path
