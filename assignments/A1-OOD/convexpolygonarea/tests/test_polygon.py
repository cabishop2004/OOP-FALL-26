"""test the Polygon class."""

import unittest

from point import Point
from polygon import Polygon


class TestPolygon(unittest.TestCase):
    """test Polygon objects."""

    def test_triangle_area(self) -> None:
        """test the area of a triangle."""
        polygon = Polygon()
        polygon.add_vertex((1, 1))
        polygon.add_vertex((2, 1))
        polygon.add_vertex((2, 2))

        self.assertEqual(polygon.area(), 0.5)

    def test_quadrilateral_area(self) -> None:
        """test the area of the sample quadrilateral."""
        polygon = Polygon()
        polygon.add_vertex((0, 0))
        polygon.add_vertex((10, 0))
        polygon.add_vertex((13, 5))
        polygon.add_vertex((10, 8))

        self.assertEqual(polygon.area(), 52.0)

    def test_area_is_independent_of_vertex_order(self) -> None:
        """test clockwise vertices still return a positive area."""
        polygon = Polygon()
        polygon.add_vertex((2, 2))
        polygon.add_vertex((2, 1))
        polygon.add_vertex((1, 1))

        self.assertEqual(polygon.area(), 0.5)

    def test_add_point_object(self) -> None:
        """test adding a Point object."""
        polygon = Polygon()
        point = Point(3, 4)

        polygon.add_vertex(point)

        self.assertEqual(polygon.vertices[0].x, 3)
        self.assertEqual(polygon.vertices[0].y, 4)

    def test_vertices_returns_copy(self) -> None:
        """test that vertices returns a copy of the list."""
        polygon = Polygon()
        polygon.add_vertex((1, 2))

        vertices = polygon.vertices
        vertices.clear()

        self.assertEqual(len(polygon.vertices), 1)


if __name__ == "__main__":
    unittest.main()
