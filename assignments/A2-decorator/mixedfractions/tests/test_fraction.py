"""test Fraction objects and fraction exceptions."""

import unittest

from hypothesis import given
from hypothesis import strategies as st

from fraction import (
    Fraction,
    MissingDenominatorError,
    ZeroDenominatorError,
)


class TestFraction(unittest.TestCase):
    """test the Fraction class."""

    def test_initial_values(self) -> None:
        """test that constructor values are stored."""
        fraction: Fraction = Fraction(27, 12)

        self.assertEqual(fraction.numerator, 27)
        self.assertEqual(fraction.denominator, 12)

    def test_change_numerator(self) -> None:
        """test changing the numerator."""
        fraction: Fraction = Fraction(1, 2)
        fraction.numerator = 9

        self.assertEqual(fraction.numerator, 9)

    def test_change_denominator(self) -> None:
        """test changing the denominator."""
        fraction: Fraction = Fraction(1, 2)
        fraction.denominator = 7

        self.assertEqual(fraction.denominator, 7)

    def test_zero_denominator_constructor(self) -> None:
        """test constructor rejects a zero denominator."""
        with self.assertRaises(ZeroDenominatorError):
            Fraction(5, 0)

    def test_zero_denominator_setter(self) -> None:
        """test setter rejects a zero denominator."""
        fraction: Fraction = Fraction(5, 2)

        with self.assertRaises(ZeroDenominatorError):
            fraction.denominator = 0

    def test_missing_denominator(self) -> None:
        """test overloaded factory rejects a missing denominator."""
        with self.assertRaises(MissingDenominatorError):
            Fraction.from_values(5)

    def test_from_two_values(self) -> None:
        """test factory creation using two integers."""
        fraction: Fraction = Fraction.from_values(8, 3)

        self.assertEqual(fraction.numerator, 8)
        self.assertEqual(fraction.denominator, 3)

    def test_from_tuple(self) -> None:
        """test factory creation using a tuple."""
        fraction: Fraction = Fraction.from_values((8, 3))

        self.assertEqual(fraction.numerator, 8)
        self.assertEqual(fraction.denominator, 3)

    def test_valid_denominator(self) -> None:
        """test denominator validation with a valid value."""
        self.assertTrue(Fraction.is_valid_denominator(4))

    def test_invalid_denominator(self) -> None:
        """test denominator validation with zero."""
        self.assertFalse(Fraction.is_valid_denominator(0))

    def test_whole_number(self) -> None:
        """test calculating a whole number portion."""
        fraction: Fraction = Fraction(27, 12)

        self.assertEqual(fraction.whole_number(), 2)

    def test_remainder(self) -> None:
        """test calculating a remainder."""
        fraction: Fraction = Fraction(27, 12)

        self.assertEqual(fraction.remainder(), 3)

    def test_mixed_parts(self) -> None:
        """test returning all mixed fraction parts."""
        fraction: Fraction = Fraction(27, 12)

        self.assertEqual(fraction.mixed_parts(), (2, 3, 12))

    def test_addition(self) -> None:
        """test fraction addition operator overloading."""
        first: Fraction = Fraction(1, 2)
        second: Fraction = Fraction(1, 3)
        result: Fraction = first + second

        self.assertEqual(result.numerator, 5)
        self.assertEqual(result.denominator, 6)

    def test_subtraction(self) -> None:
        """test fraction subtraction operator overloading."""
        first: Fraction = Fraction(3, 4)
        second: Fraction = Fraction(1, 4)
        result: Fraction = first - second

        self.assertEqual(result.numerator, 8)
        self.assertEqual(result.denominator, 16)

    def test_multiplication(self) -> None:
        """test fraction multiplication operator overloading."""
        first: Fraction = Fraction(2, 3)
        second: Fraction = Fraction(4, 5)
        result: Fraction = first * second

        self.assertEqual(result.numerator, 8)
        self.assertEqual(result.denominator, 15)

    def test_division(self) -> None:
        """test fraction division operator overloading."""
        first: Fraction = Fraction(2, 3)
        second: Fraction = Fraction(4, 5)
        result: Fraction = first / second

        self.assertEqual(result.numerator, 10)
        self.assertEqual(result.denominator, 12)

    def test_division_by_zero_fraction(self) -> None:
        """test division by a fraction with zero numerator."""
        first: Fraction = Fraction(2, 3)
        second: Fraction = Fraction(0, 5)

        with self.assertRaises(ZeroDenominatorError):
            first / second

    @given(
        numerator=st.integers(min_value=0, max_value=1_000_000),
        denominator=st.integers(min_value=1, max_value=10_000),
    )
    def test_hypothesis_mixed_parts(
        self,
        numerator: int,
        denominator: int,
    ) -> None:
        """test mixed parts using generated valid fractions."""
        fraction: Fraction = Fraction(numerator, denominator)
        whole: int
        remainder: int
        stored_denominator: int

        whole, remainder, stored_denominator = fraction.mixed_parts()

        self.assertEqual(
            numerator,
            whole * denominator + remainder,
        )
        self.assertGreaterEqual(remainder, 0)
        self.assertLess(remainder, denominator)
        self.assertEqual(stored_denominator, denominator)

    def test_whole_number_proper_fraction(self) -> None:
        """test whole number portion for a proper fraction."""
        fraction: Fraction = Fraction(3, 8)

        self.assertEqual(fraction.whole_number(), 0)

    def test_whole_number_exact_fraction(self) -> None:
        """test whole number portion for an exact fraction."""
        fraction: Fraction = Fraction(20, 4)

        self.assertEqual(fraction.whole_number(), 5)

    def test_remainder_proper_fraction(self) -> None:
        """test remainder for a proper fraction."""
        fraction: Fraction = Fraction(3, 8)

        self.assertEqual(fraction.remainder(), 3)

    def test_remainder_exact_fraction(self) -> None:
        """test remainder for an exact fraction."""
        fraction: Fraction = Fraction(20, 4)

        self.assertEqual(fraction.remainder(), 0)

    def test_mixed_parts_proper_fraction(self) -> None:
        """test mixed parts for a proper fraction."""
        fraction: Fraction = Fraction(3, 8)

        self.assertEqual(fraction.mixed_parts(), (0, 3, 8))

    def test_mixed_parts_exact_fraction(self) -> None:
        """test mixed parts for an exact fraction."""
        fraction: Fraction = Fraction(20, 4)

        self.assertEqual(fraction.mixed_parts(), (5, 0, 4))

    def test_addition_second_case(self) -> None:
        """test another fraction addition."""
        result: Fraction = Fraction(2, 5) + Fraction(3, 7)

        self.assertEqual(result.mixed_parts(), (0, 29, 35))

    def test_addition_third_case(self) -> None:
        """test fraction addition producing a whole portion."""
        result: Fraction = Fraction(3, 4) + Fraction(2, 4)

        self.assertEqual(result.numerator, 20)
        self.assertEqual(result.denominator, 16)

    def test_subtraction_second_case(self) -> None:
        """test another fraction subtraction."""
        result: Fraction = Fraction(5, 6) - Fraction(1, 3)

        self.assertEqual(result.numerator, 9)
        self.assertEqual(result.denominator, 18)

    def test_subtraction_third_case(self) -> None:
        """test subtraction producing a negative numerator."""
        result: Fraction = Fraction(1, 4) - Fraction(3, 4)

        self.assertEqual(result.numerator, -8)
        self.assertEqual(result.denominator, 16)

    def test_multiplication_second_case(self) -> None:
        """test another fraction multiplication."""
        result: Fraction = Fraction(3, 4) * Fraction(2, 7)

        self.assertEqual(result.numerator, 6)
        self.assertEqual(result.denominator, 28)

    def test_multiplication_third_case(self) -> None:
        """test multiplication by a zero numerator."""
        result: Fraction = Fraction(0, 5) * Fraction(8, 3)

        self.assertEqual(result.numerator, 0)
        self.assertEqual(result.denominator, 15)

    def test_division_second_case(self) -> None:
        """test another fraction division."""
        result: Fraction = Fraction(3, 4) / Fraction(2, 5)

        self.assertEqual(result.numerator, 15)
        self.assertEqual(result.denominator, 8)

    def test_division_third_case(self) -> None:
        """test division by an improper fraction."""
        result: Fraction = Fraction(7, 3) / Fraction(5, 2)

        self.assertEqual(result.numerator, 14)
        self.assertEqual(result.denominator, 15)


if __name__ == "__main__":
    unittest.main()
