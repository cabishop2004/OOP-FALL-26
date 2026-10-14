"""test the MixedFractionsManager class."""

import io
import unittest
from unittest.mock import patch

from mixedfractions import MixedFractionsManager


class TestMixedFractionsManager(unittest.TestCase):
    """test mixed fraction application management."""

    def test_singleton_instance(self) -> None:
        """test that instance returns the same manager."""
        first: MixedFractionsManager = MixedFractionsManager.instance()
        second: MixedFractionsManager = MixedFractionsManager.instance()

        self.assertIs(first, second)

    def test_direct_constructor_singleton(self) -> None:
        """test direct construction also uses the singleton."""
        first: MixedFractionsManager = MixedFractionsManager()
        second: MixedFractionsManager = MixedFractionsManager()

        self.assertIs(first, second)

    def test_formatter_exists(self) -> None:
        """test that the manager exposes its formatter."""
        manager: MixedFractionsManager = MixedFractionsManager.instance()

        self.assertIsNotNone(manager.formatter)

    def test_parse_line_regular_values(self) -> None:
        """test parsing a regular input line."""
        self.assertEqual(
            MixedFractionsManager.parse_line("27 12"),
            (27, 12),
        )

    def test_parse_line_large_values(self) -> None:
        """test parsing a large input line."""
        self.assertEqual(
            MixedFractionsManager.parse_line("2460000 98400"),
            (2460000, 98400),
        )

    def test_parse_line_terminator(self) -> None:
        """test parsing the terminating input line."""
        self.assertEqual(
            MixedFractionsManager.parse_line("0 0"),
            (0, 0),
        )

    def test_solve_sample(self) -> None:
        """test solving the provided Kattis sample."""
        manager: MixedFractionsManager = MixedFractionsManager.instance()
        data: str = (
            "27 12\n"
            "2460000 98400\n"
            "3 4000\n"
            "0 0\n"
        )

        self.assertEqual(
            manager.solve(data),
            "2 3 / 12\n25 0 / 98400\n0 3 / 4000",
        )

    def test_solve_stops_at_terminator(self) -> None:
        """test that input after the terminator is ignored."""
        manager: MixedFractionsManager = MixedFractionsManager.instance()
        data: str = "10 3\n0 0\n99 10\n"

        self.assertEqual(manager.solve(data), "3 1 / 3")

    def test_solve_skips_blank_lines(self) -> None:
        """test that blank input lines are ignored."""
        manager: MixedFractionsManager = MixedFractionsManager.instance()
        data: str = "\n27 12\n\n0 0\n"

        self.assertEqual(manager.solve(data), "2 3 / 12")

    def test_run_writes_output(self) -> None:
        """test running with standard input and output."""
        manager: MixedFractionsManager = MixedFractionsManager.instance()

        with patch("sys.stdin", io.StringIO("27 12\n0 0\n")):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                manager.run()

        self.assertEqual(output.getvalue(), "2 3 / 12\n")

    def test_run_empty_output(self) -> None:
        """test running with only the terminator."""
        manager: MixedFractionsManager = MixedFractionsManager.instance()

        with patch("sys.stdin", io.StringIO("0 0\n")):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                manager.run()

        self.assertEqual(output.getvalue(), "")

    def test_singleton_instance_third_reference(self) -> None:
        """test repeated instance access returns the singleton."""
        first: MixedFractionsManager = MixedFractionsManager.instance()
        second: MixedFractionsManager = MixedFractionsManager.instance()
        third: MixedFractionsManager = MixedFractionsManager.instance()

        self.assertIs(first, third)
        self.assertIs(second, third)

    def test_singleton_instance_matches_constructor(self) -> None:
        """test instance method matches direct singleton construction."""
        via_instance: MixedFractionsManager = (
            MixedFractionsManager.instance()
        )
        via_constructor: MixedFractionsManager = MixedFractionsManager()

        self.assertIs(via_instance, via_constructor)

    def test_formatter_property_is_stable(self) -> None:
        """test formatter property returns the same formatter."""
        manager: MixedFractionsManager = MixedFractionsManager.instance()

        first = manager.formatter
        second = manager.formatter

        self.assertIs(first, second)

    def test_formatter_property_formats_fraction(self) -> None:
        """test formatter property returns a usable formatter."""
        from fraction import Fraction

        manager: MixedFractionsManager = MixedFractionsManager.instance()
        fraction: Fraction = Fraction(8, 3)

        self.assertEqual(
            manager.formatter.format(fraction),
            "2 2 / 3",
        )


if __name__ == "__main__":
    unittest.main()
