"""test mixed fraction formatter classes."""

import unittest

from formatter import (
    FormatterDecorator,
    KattisSpacingDecorator,
    MixedFractionFormatter,
)
from fraction import Fraction


class TestFormatters(unittest.TestCase):
    """test formatter and decorator behavior."""

    def test_basic_formatter_regular_fraction(self) -> None:
        """test basic mixed fraction formatting."""
        formatter: MixedFractionFormatter = MixedFractionFormatter()
        fraction: Fraction = Fraction(27, 12)

        self.assertEqual(formatter.format(fraction), "2 3/12")

    def test_basic_formatter_proper_fraction(self) -> None:
        """test basic formatting with no whole portion."""
        formatter: MixedFractionFormatter = MixedFractionFormatter()
        fraction: Fraction = Fraction(3, 4000)

        self.assertEqual(formatter.format(fraction), "0 3/4000")

    def test_basic_formatter_exact_fraction(self) -> None:
        """test basic formatting with no remainder."""
        formatter: MixedFractionFormatter = MixedFractionFormatter()
        fraction: Fraction = Fraction(20, 4)

        self.assertEqual(formatter.format(fraction), "5 0/4")

    def test_base_decorator_delegates(self) -> None:
        """test that the base decorator delegates formatting."""
        formatter: FormatterDecorator = FormatterDecorator(
            MixedFractionFormatter()
        )
        fraction: Fraction = Fraction(27, 12)

        self.assertEqual(formatter.format(fraction), "2 3/12")

    def test_decorator_formatter_property(self) -> None:
        """test access to the wrapped formatter."""
        wrapped: MixedFractionFormatter = MixedFractionFormatter()
        decorator: FormatterDecorator = FormatterDecorator(wrapped)

        self.assertIs(decorator.formatter, wrapped)

    def test_kattis_spacing_regular_fraction(self) -> None:
        """test Kattis formatting for a mixed fraction."""
        formatter: KattisSpacingDecorator = KattisSpacingDecorator(
            MixedFractionFormatter()
        )
        fraction: Fraction = Fraction(27, 12)

        self.assertEqual(formatter.format(fraction), "2 3 / 12")

    def test_kattis_spacing_proper_fraction(self) -> None:
        """test Kattis formatting for a proper fraction."""
        formatter: KattisSpacingDecorator = KattisSpacingDecorator(
            MixedFractionFormatter()
        )
        fraction: Fraction = Fraction(3, 4000)

        self.assertEqual(formatter.format(fraction), "0 3 / 4000")

    def test_kattis_spacing_exact_fraction(self) -> None:
        """test Kattis formatting for an exact whole number."""
        formatter: KattisSpacingDecorator = KattisSpacingDecorator(
            MixedFractionFormatter()
        )
        fraction: Fraction = Fraction(2460000, 98400)

        self.assertEqual(formatter.format(fraction), "25 0 / 98400")

    def test_base_decorator_proper_fraction(self) -> None:
        """test base decorator formatting a proper fraction."""
        formatter: FormatterDecorator = FormatterDecorator(
            MixedFractionFormatter()
        )
        fraction: Fraction = Fraction(3, 8)

        self.assertEqual(formatter.format(fraction), "0 3/8")

    def test_base_decorator_exact_fraction(self) -> None:
        """test base decorator formatting an exact fraction."""
        formatter: FormatterDecorator = FormatterDecorator(
            MixedFractionFormatter()
        )
        fraction: Fraction = Fraction(20, 4)

        self.assertEqual(formatter.format(fraction), "5 0/4")

    def test_decorator_formatter_property_second_case(self) -> None:
        """test the wrapped formatter property with another formatter."""
        wrapped: MixedFractionFormatter = MixedFractionFormatter()
        decorator: FormatterDecorator = FormatterDecorator(wrapped)

        self.assertIs(decorator.formatter, wrapped)

    def test_decorator_formatter_property_third_case(self) -> None:
        """test the wrapped formatter property remains stable."""
        wrapped: MixedFractionFormatter = MixedFractionFormatter()
        decorator: FormatterDecorator = FormatterDecorator(wrapped)

        first = decorator.formatter
        second = decorator.formatter

        self.assertIs(first, second)


if __name__ == "__main__":
    unittest.main()
