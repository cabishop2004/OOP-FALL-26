"""define formatters and decorators for mixed fractions."""

from abc import ABC, abstractmethod

from fraction import Fraction


class FractionFormatter(ABC):
    """define the public interface for fraction formatting."""

    @abstractmethod
    def format(self, fraction: Fraction) -> str:
        """format a fraction as text."""


class MixedFractionFormatter(FractionFormatter):
    """format a fraction in basic mixed fraction form."""

    def format(self, fraction: Fraction) -> str:
        """format a fraction without spaces around the slash."""
        whole: int
        remainder: int
        denominator: int

        whole, remainder, denominator = fraction.mixed_parts()

        return f"{whole} {remainder}/{denominator}"


class FormatterDecorator(FractionFormatter):
    """provide the base decorator for fraction formatters."""

    def __init__(self, formatter: FractionFormatter) -> None:
        """initialize the decorator with another formatter."""
        self.__formatter: FractionFormatter = formatter

    @property
    def formatter(self) -> FractionFormatter:
        """return the wrapped formatter."""
        return self.__formatter

    def format(self, fraction: Fraction) -> str:
        """delegate formatting to the wrapped formatter."""
        return self.__formatter.format(fraction)


class KattisSpacingDecorator(FormatterDecorator):
    """decorate mixed fraction output for Kattis spacing."""

    def format(self, fraction: Fraction) -> str:
        """add spaces around the fraction slash."""
        formatted: str = super().format(fraction)

        return formatted.replace("/", " / ")
