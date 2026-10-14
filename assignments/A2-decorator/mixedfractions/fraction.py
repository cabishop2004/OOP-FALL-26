"""define fraction objects and fraction related exceptions."""

from __future__ import annotations

from typing import overload


class FractionError(ValueError):
    """represent a general fraction error."""


class ZeroDenominatorError(FractionError):
    """represent an invalid fraction with a zero denominator."""


class MissingDenominatorError(FractionError):
    """represent a missing denominator value."""


class Fraction:
    """represent a fraction using a numerator and denominator."""

    def __init__(self, numerator: int, denominator: int) -> None:
        """initialize a fraction."""
        self.__numerator: int = numerator
        self.__denominator: int = 1
        self.denominator = denominator

    @property
    def numerator(self) -> int:
        """return the numerator."""
        return self.__numerator

    @numerator.setter
    def numerator(self, value: int) -> None:
        """set the numerator."""
        self.__numerator = value

    @property
    def denominator(self) -> int:
        """return the denominator."""
        return self.__denominator

    @denominator.setter
    def denominator(self, value: int) -> None:
        """set the denominator."""
        if value == 0:
            raise ZeroDenominatorError("denominator cannot be zero")

        self.__denominator = value

    @classmethod
    @overload
    def from_values(cls, numerator: int, denominator: int) -> Fraction:
        ...

    @classmethod
    @overload
    def from_values(cls, numerator: tuple[int, int]) -> Fraction:
        ...

    @classmethod
    @overload
    def from_values(
        cls,
        numerator: int,
        denominator: None = None,
    ) -> Fraction:
        ...

    @classmethod
    def from_values(
        cls,
        numerator: int | tuple[int, int],
        denominator: int | None = None,
    ) -> Fraction:
        """create a fraction from two integers or an integer pair."""
        if isinstance(numerator, tuple):
            return cls(numerator[0], numerator[1])

        if denominator is None:
            raise MissingDenominatorError("denominator is required")

        return cls(numerator, denominator)

    @staticmethod
    def is_valid_denominator(value: int) -> bool:
        """return whether a denominator is valid."""
        return value != 0

    def whole_number(self) -> int:
        """return the whole number portion of the fraction."""
        return self.__numerator // self.__denominator

    def remainder(self) -> int:
        """return the remainder portion of the fraction."""
        return self.__numerator % self.__denominator

    def mixed_parts(self) -> tuple[int, int, int]:
        """return the whole number, remainder, and denominator."""
        return (
            self.whole_number(),
            self.remainder(),
            self.__denominator,
        )

    def __add__(self, other: Fraction) -> Fraction:
        """return the sum of two fractions."""
        numerator: int = (
            self.__numerator * other.denominator
            + other.numerator * self.__denominator
        )
        denominator: int = self.__denominator * other.denominator

        return Fraction(numerator, denominator)

    def __sub__(self, other: Fraction) -> Fraction:
        """return the difference between two fractions."""
        numerator: int = (
            self.__numerator * other.denominator
            - other.numerator * self.__denominator
        )
        denominator: int = self.__denominator * other.denominator

        return Fraction(numerator, denominator)

    def __mul__(self, other: Fraction) -> Fraction:
        """return the product of two fractions."""
        numerator: int = self.__numerator * other.numerator
        denominator: int = self.__denominator * other.denominator

        return Fraction(numerator, denominator)

    def __truediv__(self, other: Fraction) -> Fraction:
        """return the quotient of two fractions."""
        numerator: int = self.__numerator * other.denominator
        denominator: int = self.__denominator * other.numerator

        return Fraction(numerator, denominator)
