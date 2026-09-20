"""solve the Kattis Convex Polygon Area problem using objects."""

from __future__ import annotations

import sys
from typing import ClassVar

from polygon import Polygon


class ConvexPolygonAreaApp:
    """manage input, output, and polygon area calculations."""

    __instance: ClassVar[ConvexPolygonAreaApp | None] = None

    def __new__(cls) -> ConvexPolygonAreaApp:
        """return the single application instance."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def instance(cls) -> ConvexPolygonAreaApp:
        """return the singleton application instance."""
        return cls()

    @staticmethod
    def format_area(area: float) -> str:
        """format an area for Kattis output."""
        if area.is_integer():
            return str(int(area))

        return str(area)

    def solve(self, data: str) -> str:
        """solve polygon area input and return formatted output."""
        lines: list[str] = [
            line.strip()
            for line in data.splitlines()
            if line.strip()
        ]

        if not lines:
            return ""

        polygon_count: int = int(lines[0])
        results: list[str] = []

        for line in lines[1:polygon_count + 1]:
            values: list[int] = [int(value) for value in line.split()]
            vertex_count: int = values[0]
            polygon: Polygon = Polygon()

            for index in range(vertex_count):
                coordinate_index: int = 1 + (index * 2)
                x: int = values[coordinate_index]
                y: int = values[coordinate_index + 1]
                polygon.add_vertex((x, y))

            results.append(self.format_area(polygon.area()))

        return "\n".join(results)

    def run(self) -> None:
        """read standard input, solve the problem, and print the result."""
        result: str = self.solve(sys.stdin.read())

        if result:
            sys.stdout.write(f"{result}\n")


if __name__ == "__main__":
    ConvexPolygonAreaApp.instance().run()
