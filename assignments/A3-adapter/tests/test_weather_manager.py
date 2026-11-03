"""test singleton weather management and adapter coordination."""

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from weather_adapter import WeatherAdapter, WeatherData
from weather_client import WeatherClient
from weather_manager import WeatherManager


SAMPLE_PAYLOAD: dict[str, object] = {
    "latitude": 39.064,
    "longitude": -108.551,
    "current": {
        "temperature_2m": 71.5,
        "relative_humidity_2m": 32,
        "wind_speed_10m": 8.4,
        "precipitation": 0.01,
        "weather_code": 2,
    },
}


def make_weather() -> WeatherData:
    """create normalized test weather."""
    return WeatherData(
        39.064,
        -108.551,
        71.5,
        32,
        8.4,
        0.01,
        2,
    )


class TestWeatherManager(unittest.TestCase):
    """test the weather manager singleton."""

    def test_instance_returns_same_object(self) -> None:
        """test repeated singleton access."""
        first = WeatherManager.instance()
        second = WeatherManager.instance()

        self.assertIs(first, second)

    def test_instance_matches_constructor(self) -> None:
        """test class API matches direct construction."""
        self.assertIs(
            WeatherManager.instance(),
            WeatherManager(),
        )

    def test_instance_third_reference(self) -> None:
        """test singleton remains stable across references."""
        first = WeatherManager.instance()
        second = WeatherManager.instance()
        third = WeatherManager.instance()

        self.assertIs(first, third)
        self.assertIs(second, third)

    @patch.object(
        WeatherAdapter,
        "adapt",
    )
    @patch.object(
        WeatherClient,
        "fetch_current",
    )
    def test_get_current_weather_returns_adapter_result(
        self,
        mocked_fetch: Mock,
        mocked_adapt: Mock,
    ) -> None:
        """test manager returns normalized adapter output."""
        weather = make_weather()
        mocked_fetch.return_value = SAMPLE_PAYLOAD
        mocked_adapt.return_value = weather

        result = WeatherManager.instance().get_current_weather(
            39.064,
            -108.551,
        )

        self.assertIs(result, weather)

    @patch.object(
        WeatherAdapter,
        "adapt",
    )
    @patch.object(
        WeatherClient,
        "fetch_current",
    )
    def test_get_current_weather_passes_coordinates(
        self,
        mocked_fetch: Mock,
        mocked_adapt: Mock,
    ) -> None:
        """test manager sends coordinates to the client."""
        mocked_fetch.return_value = SAMPLE_PAYLOAD
        mocked_adapt.return_value = make_weather()

        WeatherManager.instance().get_current_weather(
            40.0,
            -105.0,
        )

        mocked_fetch.assert_called_once_with(
            40.0,
            -105.0,
        )

    @patch.object(
        WeatherAdapter,
        "adapt",
    )
    @patch.object(
        WeatherClient,
        "fetch_current",
    )
    def test_get_current_weather_passes_payload(
        self,
        mocked_fetch: Mock,
        mocked_adapt: Mock,
    ) -> None:
        """test manager sends client data to the adapter."""
        mocked_fetch.return_value = SAMPLE_PAYLOAD
        mocked_adapt.return_value = make_weather()

        WeatherManager.instance().get_current_weather(
            39.0,
            -108.0,
        )

        mocked_adapt.assert_called_once_with(
            SAMPLE_PAYLOAD
        )


if __name__ == "__main__":
    unittest.main()
