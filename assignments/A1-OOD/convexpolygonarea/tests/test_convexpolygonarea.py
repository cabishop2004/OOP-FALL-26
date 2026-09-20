"""test the ConvexPolygonAreaApp class."""

import unittest

from convexpolygonarea import ConvexPolygonAreaApp


class TestConvexPolygonAreaApp(unittest.TestCase):
    """test the ConvexPolygonAreaApp class."""

    def test_singleton_instance(self) -> None:
        """test that instance returns the same object."""
        first = ConvexPolygonAreaApp.instance()
        second = ConvexPolygonAreaApp.instance()

        self.assertIs(first, second)

    def test_constructor_uses_singleton(self) -> None:
        """test that direct construction returns the same object."""
        first = ConvexPolygonAreaApp()
        second = ConvexPolygonAreaApp.instance()

        self.assertIs(first, second)

    def test_format_integer_area(self) -> None:
        """test formatting an integer area."""
        result = ConvexPolygonAreaApp.format_area(52.0)

        self.assertEqual(result, "52")

    def test_format_half_area(self) -> None:
        """test formatting an area ending in one half."""
        result = ConvexPolygonAreaApp.format_area(0.5)

        self.assertEqual(result, "0.5")

    def test_format_decimal_area(self) -> None:
        """test formatting another decimal area."""
        result = ConvexPolygonAreaApp.format_area(12.25)

        self.assertEqual(result, "12.25")

    def test_solve_triangle(self) -> None:
        """test solving a single triangle."""
        app = ConvexPolygonAreaApp.instance()
        data = "1\n3 1 1 2 1 2 2\n"

        self.assertEqual(app.solve(data), "0.5")

    def test_solve_square(self) -> None:
        """test solving a single square."""
        app = ConvexPolygonAreaApp.instance()
        data = "1\n4 0 0 2 0 2 2 0 2\n"

        self.assertEqual(app.solve(data), "4")

    def test_solve_sample(self) -> None:
        """test solving the provided Kattis sample."""
        app = ConvexPolygonAreaApp.instance()
        data = (
            "2\n"
            "3 1 1 2 1 2 2\n"
            "4 0 0 10 0 13 5 10 8\n"
        )

        self.assertEqual(app.solve(data), "0.5\n52")

    def test_solve_empty_input(self) -> None:
        """test solving empty input."""
        app = ConvexPolygonAreaApp.instance()

        self.assertEqual(app.solve(""), "")


if __name__ == "__main__":
    unittest.main()
