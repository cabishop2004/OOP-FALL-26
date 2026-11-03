"""test the Open-Meteo HTTP client with mocked requests."""

from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

import requests

from weather_client import (
    BASE_URL,
    DEFAULT_TIMEOUT,
    WeatherClient,
    WeatherClientError,
)


SAMPLE_RESPONSE: dict[str, object] = {
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


class TestWeatherClient(unittest.TestCase):
    """test the external weather API client."""

    def test_default_properties(self) -> None:
        """test default client configuration."""
        client = WeatherClient()

        self.assertEqual(client.base_url, BASE_URL)
        self.assertEqual(client.timeout, DEFAULT_TIMEOUT)

    def test_custom_properties(self) -> None:
        """test custom client configuration."""
        client = WeatherClient(
            "https://example.com/weather",
            5.0,
        )

        self.assertEqual(
            client.base_url,
            "https://example.com/weather",
        )
        self.assertEqual(client.timeout, 5.0)

    def test_properties_third_configuration(self) -> None:
        """test client properties with a third configuration."""
        client = WeatherClient(
            "https://weather.example/api",
            15.5,
        )

        self.assertEqual(
            client.base_url,
            "https://weather.example/api",
        )
        self.assertEqual(client.timeout, 15.5)

    def test_empty_base_url(self) -> None:
        """test rejection of an empty base URL."""
        with self.assertRaises(ValueError):
            WeatherClient("")

    def test_invalid_timeout(self) -> None:
        """test rejection of a nonpositive timeout."""
        with self.assertRaises(ValueError):
            WeatherClient(timeout=0)

    def test_valid_coordinates(self) -> None:
        """test normal valid coordinates."""
        self.assertTrue(
            WeatherClient.coordinates_are_valid(
                39.064,
                -108.551,
            )
        )

    def test_invalid_latitude(self) -> None:
        """test invalid latitude."""
        self.assertFalse(
            WeatherClient.coordinates_are_valid(
                91.0,
                0.0,
            )
        )

    def test_invalid_longitude(self) -> None:
        """test invalid longitude."""
        self.assertFalse(
            WeatherClient.coordinates_are_valid(
                0.0,
                -181.0,
            )
        )

    @patch("weather_client.requests.get")
    def test_fetch_current_success(
        self,
        mocked_get: Mock,
    ) -> None:
        """test successful API weather retrieval."""
        response = Mock()
        response.json.return_value = SAMPLE_RESPONSE
        mocked_get.return_value = response

        result = WeatherClient().fetch_current(
            39.064,
            -108.551,
        )

        self.assertEqual(result, SAMPLE_RESPONSE)

        mocked_get.assert_called_once()

        call_kwargs = mocked_get.call_args.kwargs

        self.assertEqual(
            call_kwargs["params"]["latitude"],
            39.064,
        )
        self.assertEqual(
            call_kwargs["params"]["longitude"],
            -108.551,
        )

    def test_fetch_current_invalid_coordinates(self) -> None:
        """test weather retrieval with invalid coordinates."""
        client = WeatherClient()

        with self.assertRaises(ValueError):
            client.fetch_current(
                100.0,
                -108.0,
            )

    @patch("weather_client.requests.get")
    def test_fetch_current_http_error(
        self,
        mocked_get: Mock,
    ) -> None:
        """test conversion of an HTTP failure."""
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError(
            "server error"
        )
        mocked_get.return_value = response

        with self.assertRaises(WeatherClientError):
            WeatherClient().fetch_current(
                39.0,
                -108.0,
            )

    @patch("weather_client.requests.get")
    def test_fetch_current_invalid_json(
        self,
        mocked_get: Mock,
    ) -> None:
        """test conversion of invalid JSON."""
        response = Mock()
        response.json.side_effect = ValueError(
            "invalid JSON"
        )
        mocked_get.return_value = response

        with self.assertRaises(WeatherClientError):
            WeatherClient().fetch_current(
                39.0,
                -108.0,
            )

    @patch("weather_client.requests.get")
    def test_fetch_current_unexpected_response(
        self,
        mocked_get: Mock,
    ) -> None:
        """test rejection of a nonobject API response."""
        response = Mock()
        response.json.return_value = []
        mocked_get.return_value = response

        with self.assertRaises(WeatherClientError):
            WeatherClient().fetch_current(
                39.0,
                -108.0,
            )


if __name__ == "__main__":
    unittest.main()
