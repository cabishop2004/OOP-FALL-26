"""define a polygon made from Point objects."""

from typing import overload

from point import Point


class Polygon:
    """represent a polygon and calculate its area."""

    def __init__(self) -> None:
        """initialize an empty polygon."""
        self.__vertices: list[Point] = []

    @property
    def vertices(self) -> list[Point]:
        """return a copy of the polygon vertices."""
        return self.__vertices.copy()

    @overload
    def add_vertex(self, point: Point) -> None:
        ...

    @overload
    def add_vertex(self, point: tuple[int, int]) -> None:
        ...

    def add_vertex(self, point: Point | tuple[int, int]) -> None:
        """add a Point object or coordinate pair to the polygon."""
        if isinstance(point, Point):
            self.__vertices.append(point)
        else:
            self.__vertices.append(Point(point[0], point[1]))

    def area(self) -> float:
        """calculate polygon area using the shoelace formula."""
        total: int = 0
        vertex_count: int = len(self.__vertices)

        for index in range(vertex_count):
            current: Point = self.__vertices[index]
            next_point: Point = self.__vertices[(index + 1) % vertex_count]

            total += current.x * next_point.y
            total -= current.y * next_point.x

        return abs(total) / 2
