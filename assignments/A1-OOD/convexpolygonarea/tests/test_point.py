"""test the Point class."""

import unittest

from point import Point


class TestPoint(unittest.TestCase):
    """test Point objects."""

    def test_initial_coordinates(self) -> None:
        """test that initial coordinates are stored correctly."""
        point = Point(3, 4)

        self.assertEqual(point.x, 3)
        self.assertEqual(point.y, 4)

    def test_set_x(self) -> None:
        """test changing the x coordinate."""
        point = Point(1, 2)

        point.x = 7

        self.assertEqual(point.x, 7)

    def test_set_y(self) -> None:
        """test changing the y coordinate."""
        point = Point(1, 2)

        point.y = 9

        self.assertEqual(point.y, 9)


if __name__ == "__main__":
    unittest.main()
