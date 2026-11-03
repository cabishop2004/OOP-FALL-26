"""provide a Rich command line interface for current weather."""

from __future__ import annotations

from argparse import ArgumentParser
from collections.abc import Sequence

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from weather_adapter import WeatherAdapterError, WeatherData
from weather_client import WeatherClientError
from weather_manager import WeatherManager


class WeatherApp:
    """display normalized weather data through a Rich CLI."""

    def __init__(
        self,
        manager: WeatherManager | None = None,
        console: Console | None = None,
    ) -> None:
        """initialize the weather application."""
        self.__manager: WeatherManager = (
            manager or WeatherManager.instance()
        )
        self.__console: Console = console or Console()

    def run(
        self,
        latitude: float,
        longitude: float,
    ) -> None:
        """retrieve weather data and display it using Rich."""
        try:
            weather: WeatherData = self.__manager.get_current_weather(
                latitude,
                longitude,
            )
        except (
            WeatherClientError,
            WeatherAdapterError,
            ValueError,
        ) as error:
            self.__console.print(
                Panel(
                    str(error),
                    title="Weather Error",
                    border_style="red",
                )
            )
            return

        table = Table(
            title="Current Weather",
            show_header=True,
            header_style="bold",
        )

        table.add_column("Metric")
        table.add_column("Value", justify="right")

        table.add_row(
            "Location",
            f"{weather.latitude:.4f}, {weather.longitude:.4f}",
        )
        table.add_row(
            "Temperature",
            f"{weather.temperature:.1f} °F",
        )
        table.add_row(
            "Relative Humidity",
            f"{weather.humidity}%",
        )
        table.add_row(
            "Wind Speed",
            f"{weather.wind_speed:.1f} mph",
        )
        table.add_row(
            "Precipitation",
            f"{weather.precipitation:.3f} in",
        )
        table.add_row(
            "WMO Weather Code",
            str(weather.weather_code),
        )

        self.__console.print(
            Panel(
                table,
                title="Open-Meteo Weather",
                subtitle="Adapter Pattern Demo",
            )
        )


def main(args: Sequence[str] | None = None) -> None:
    """parse CLI arguments and run the weather application."""
    parser = ArgumentParser(
        description="Display current weather using Open-Meteo."
    )

    parser.add_argument(
        "latitude",
        type=float,
        help="latitude from -90 to 90",
    )

    parser.add_argument(
        "longitude",
        type=float,
        help="longitude from -180 to 180",
    )

    parsed = parser.parse_args(args)

    WeatherApp().run(
        parsed.latitude,
        parsed.longitude,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
