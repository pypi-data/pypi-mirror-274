import heapq
import math
from typing import List

from fuel_efficiency.algorithms.path_finding import PathfindingStrategy
from fuel_efficiency.entities.node import Node
from fuel_efficiency.entities.position import Position


class DijkstraStrategy(PathfindingStrategy):

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
        rows, cols = len(grid), len(grid[0])
        distances = [[float('inf')] * cols for _ in range(rows)]
        distances[start.position.x][start.position.y] = grid[start.position.x][
            start.position.y
        ].weight

        previous = [[None] * cols for _ in range(rows)]

        pq = [(grid[start.position.x][start.position.y].weight, start)]

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

            for neighbor in DijkstraStrategy.get_neighbors(grid, current_node):
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
        # Euclidean distance
        return math.sqrt(
            (node2.position.x - node1.position.x) ** 2
            + (node2.position.y - node1.position.y) ** 2
        )
