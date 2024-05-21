import heapq
from typing import List, Tuple

from fuel_efficiency.algorithms.path_finding import PathfindingStrategy
from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.position import Position


class AStarStrategy(PathfindingStrategy):
    """
    A class used to represent a Position (x,y)

    A ``Position(x,y)`` is a position on a grid with x axis and y axis.

    This class uses ``dataclasses`` that provides a decorator and functions for automatically adding generated special
    methods such as ``__init__()`` and ``__repr__()``

    Attributes:
        x (int): position value on x-axis
        y (int): position value on x-axis
    """

    allowed_directions = [
        Position(-1, 0),
        Position(0, -1),
        Position(0, 1),
        Position(1, 0),
    ]

    def find_path(grid: List[List[Node]], start: Node, end: Node):
        rows, cols = len(grid), len(grid[0])
        distances = [[float('inf')] * cols for _ in range(rows)]
        distances[start.position.x][start.position.y] = grid[start.position.x][
            start.position.y
        ].weight

        previous = [[None] * cols for _ in range(rows)]

        pq = [
            (
                grid[start.position.x][start.position.y].weight
                + AStarStrategy.calculate_distance(start, end),
                start,
            )
        ]
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

                for neighbor in AStarStrategy.get_neighbors(
                    grid, current_node
                ):
                    new_distance = current_distance + neighbor.weight

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
                        heapq.heappush(
                            pq,
                            (
                                new_distance
                                + AStarStrategy.calculate_distance(
                                    neighbor, end
                                ),
                                neighbor,
                            ),
                        )

        return []

    def get_neighbors(grid: List[List[Node]], node: Node) -> List[Node]:
        neighbors_list = []
        grid_xlen = len(grid)
        grid_ylen = len(grid[0])
        for direction in AStarStrategy.allowed_directions:
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
        # Manhattan distance
        return abs(node1.position.x - node2.position.x) + abs(
            node1.position.y - node2.position.y
        )

    def calculate_fuel_consumption(
        grid: List[List[Node]], start: Node, end: Node
    ) -> Tuple[float, List[Node]]:
        path = AStarStrategy.find_path(grid, start, end)
        fuel_consumption = 0
        for node in path:
            fuel_consumption += node.weight
        return fuel_consumption, path
