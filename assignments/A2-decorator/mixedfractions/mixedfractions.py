"""solve the Kattis Mixed Fractions problem using object-oriented design."""

from __future__ import annotations

import sys
from typing import ClassVar

from formatter import (
    FractionFormatter,
    KattisSpacingDecorator,
    MixedFractionFormatter,
)
from fraction import Fraction


class MixedFractionsManager:
    """manage mixed fraction input, conversion, and output."""

    __instance: ClassVar[MixedFractionsManager | None] = None

    def __new__(cls) -> MixedFractionsManager:
        """return the single manager instance."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        """initialize the manager with its output formatter."""
        if not hasattr(self, "_MixedFractionsManager__formatter"):
            self.__formatter: FractionFormatter = KattisSpacingDecorator(
                MixedFractionFormatter()
            )

    @classmethod
    def instance(cls) -> MixedFractionsManager:
        """return the singleton manager instance."""
        return cls()

    @property
    def formatter(self) -> FractionFormatter:
        """return the configured fraction formatter."""
        return self.__formatter

    @staticmethod
    def parse_line(line: str) -> tuple[int, int]:
        """convert one input line into numerator and denominator values."""
        values: list[int] = [int(value) for value in line.split()]

        return values[0], values[1]

    def solve(self, data: str) -> str:
        """convert Kattis input into mixed fraction output."""
        results: list[str] = []

        for line in data.splitlines():
            if not line.strip():
                continue

            numerator: int
            denominator: int
            numerator, denominator = self.parse_line(line)

            if numerator == 0 and denominator == 0:
                break

            fraction: Fraction = Fraction(numerator, denominator)
            results.append(self.__formatter.format(fraction))

        return "\n".join(results)

    def run(self) -> None:
        """read standard input and write the solution."""
        result: str = self.solve(sys.stdin.read())

        if result:
            sys.stdout.write(f"{result}\n")


if __name__ == "__main__":  # pragma: no cover
    MixedFractionsManager.instance().run()
