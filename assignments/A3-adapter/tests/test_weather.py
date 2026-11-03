"""test the Rich weather command line application."""

from __future__ import annotations

import io
import unittest
from unittest.mock import Mock, patch

from rich.console import Console

from weather import WeatherApp, main
from weather_adapter import WeatherAdapterError, WeatherData
from weather_client import WeatherClientError
from weather_manager import WeatherManager


def make_console(
    stream: io.StringIO,
) -> Console:
    """create a deterministic Rich console for tests."""
    return Console(
        file=stream,
        force_terminal=False,
        color_system=None,
        width=100,
    )


def make_weather() -> WeatherData:
    """create weather data for UI tests."""
    return WeatherData(
        39.064,
        -108.551,
        71.5,
        32,
        8.4,
        0.01,
        2,
    )


class TestWeatherApp(unittest.TestCase):
    """test the Rich command line interface."""

    @patch.object(
        WeatherManager,
        "get_current_weather",
    )
    def test_run_displays_weather(
        self,
        mocked_weather: Mock,
    ) -> None:
        """test successful Rich weather display."""
        mocked_weather.return_value = make_weather()

        stream = io.StringIO()
        app = WeatherApp(
            manager=WeatherManager.instance(),
            console=make_console(stream),
        )

        app.run(
            39.064,
            -108.551,
        )

        output = stream.getvalue()

        self.assertIn("Current Weather", output)
        self.assertIn("71.5", output)
        self.assertIn("Relative Humidity", output)

    @patch.object(
        WeatherManager,
        "get_current_weather",
    )
    def test_run_displays_client_error(
        self,
        mocked_weather: Mock,
    ) -> None:
        """test Rich display for a client failure."""
        mocked_weather.side_effect = WeatherClientError(
            "unable to retrieve weather data"
        )

        stream = io.StringIO()
        app = WeatherApp(
            manager=WeatherManager.instance(),
            console=make_console(stream),
        )

        app.run(
            39.0,
            -108.0,
        )

        output = stream.getvalue()

        self.assertIn("Weather Error", output)
        self.assertIn(
            "unable to retrieve weather data",
            output,
        )

    @patch.object(
        WeatherManager,
        "get_current_weather",
    )
    def test_run_displays_adapter_error(
        self,
        mocked_weather: Mock,
    ) -> None:
        """test Rich display for invalid API data."""
        mocked_weather.side_effect = WeatherAdapterError(
            "invalid weather data"
        )

        stream = io.StringIO()
        app = WeatherApp(
            manager=WeatherManager.instance(),
            console=make_console(stream),
        )

        app.run(
            39.0,
            -108.0,
        )

        output = stream.getvalue()

        self.assertIn("Weather Error", output)
        self.assertIn(
            "invalid weather data",
            output,
        )

    @patch("weather.WeatherApp")
    def test_main_runs_application(
        self,
        mocked_app_class: Mock,
    ) -> None:
        """test command line argument processing."""
        mocked_app = mocked_app_class.return_value

        main(
            [
                "39.064",
                "-108.551",
            ]
        )

        mocked_app.run.assert_called_once_with(
            39.064,
            -108.551,
        )

    @patch("weather.WeatherApp")
    def test_main_runs_application_second_coordinates(
        self,
        mocked_app_class: Mock,
    ) -> None:
        """test command line parsing with another coordinate pair."""
        mocked_app = mocked_app_class.return_value

        main(
            [
                "40.0150",
                "-105.2705",
            ]
        )

        mocked_app.run.assert_called_once_with(
            40.015,
            -105.2705,
        )

    @patch("weather.WeatherApp")
    def test_main_runs_application_boundary_coordinates(
        self,
        mocked_app_class: Mock,
    ) -> None:
        """test command line parsing with coordinate boundaries."""
        mocked_app = mocked_app_class.return_value

        main(
            [
                "90",
                "180",
            ]
        )

        mocked_app.run.assert_called_once_with(
            90.0,
            180.0,
        )


if __name__ == "__main__":
    unittest.main()
