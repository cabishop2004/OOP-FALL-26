"""test weather data objects and the Open-Meteo adapter."""

from __future__ import annotations

import copy
import json
import unittest
from typing import cast

from hypothesis import given
from hypothesis import strategies as st

from weather_adapter import (
    REQUIRED_CURRENT_FIELDS,
    WeatherAdapter,
    WeatherAdapterError,
    WeatherData,
)


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


class TestWeatherData(unittest.TestCase):
    """test normalized weather data."""

    def test_weather_data_properties(self) -> None:
        """test all normalized weather properties."""
        weather = WeatherData(
            39.064,
            -108.551,
            71.5,
            32,
            8.4,
            0.01,
            2,
        )

        self.assertEqual(weather.latitude, 39.064)
        self.assertEqual(weather.longitude, -108.551)
        self.assertEqual(weather.temperature, 71.5)
        self.assertEqual(weather.humidity, 32)
        self.assertEqual(weather.wind_speed, 8.4)
        self.assertEqual(weather.precipitation, 0.01)
        self.assertEqual(weather.weather_code, 2)

    def test_weather_data_properties_second_case(self) -> None:
        """test normalized weather properties with another data set."""
        weather = WeatherData(
            0.0,
            0.0,
            32.0,
            100,
            0.0,
            1.25,
            61,
        )

        self.assertEqual(weather.latitude, 0.0)
        self.assertEqual(weather.longitude, 0.0)
        self.assertEqual(weather.temperature, 32.0)
        self.assertEqual(weather.humidity, 100)
        self.assertEqual(weather.wind_speed, 0.0)
        self.assertEqual(weather.precipitation, 1.25)
        self.assertEqual(weather.weather_code, 61)

    def test_weather_data_properties_third_case(self) -> None:
        """test normalized weather properties with negative values."""
        weather = WeatherData(
            -33.8688,
            151.2093,
            55.2,
            64,
            12.3,
            0.0,
            3,
        )

        self.assertEqual(weather.latitude, -33.8688)
        self.assertEqual(weather.longitude, 151.2093)
        self.assertEqual(weather.temperature, 55.2)
        self.assertEqual(weather.humidity, 64)
        self.assertEqual(weather.wind_speed, 12.3)
        self.assertEqual(weather.precipitation, 0.0)
        self.assertEqual(weather.weather_code, 3)


class TestWeatherAdapter(unittest.TestCase):
    """test conversion of third party weather data."""

    def setUp(self) -> None:
        """create an adapter before each test."""
        self.adapter = WeatherAdapter()

    def test_required_fields_match_constant(self) -> None:
        """test required field class API."""
        self.assertEqual(
            WeatherAdapter.required_current_fields(),
            REQUIRED_CURRENT_FIELDS,
        )

    def test_required_fields_contains_temperature(self) -> None:
        """test required fields contain temperature."""
        self.assertIn(
            "temperature_2m",
            WeatherAdapter.required_current_fields(),
        )

    def test_required_fields_contains_weather_code(self) -> None:
        """test required fields contain weather code."""
        self.assertIn(
            "weather_code",
            WeatherAdapter.required_current_fields(),
        )

    def test_supported_payload(self) -> None:
        """test recognition of a complete payload."""
        self.assertTrue(
            WeatherAdapter.is_supported(SAMPLE_PAYLOAD)
        )

    def test_unsupported_payload_without_current(self) -> None:
        """test rejection when current data is missing."""
        payload: dict[str, object] = {
            "latitude": 39.0,
            "longitude": -108.0,
        }

        self.assertFalse(
            WeatherAdapter.is_supported(payload)
        )

    def test_unsupported_payload_missing_field(self) -> None:
        """test rejection when a current field is missing."""
        payload = copy.deepcopy(SAMPLE_PAYLOAD)
        current = cast(
            dict[str, object],
            payload["current"],
        )
        current.pop("weather_code")

        self.assertFalse(
            WeatherAdapter.is_supported(payload)
        )

    def test_adapt_mapping(self) -> None:
        """test adapting an API mapping."""
        weather = self.adapter.adapt(SAMPLE_PAYLOAD)

        self.assertEqual(weather.temperature, 71.5)
        self.assertEqual(weather.humidity, 32)

    def test_adapt_json_string(self) -> None:
        """test adapting API JSON text."""
        weather = self.adapter.adapt(
            json.dumps(SAMPLE_PAYLOAD)
        )

        self.assertEqual(weather.wind_speed, 8.4)
        self.assertEqual(weather.weather_code, 2)

    def test_adapt_missing_required_field(self) -> None:
        """test adapting an incomplete payload."""
        payload = copy.deepcopy(SAMPLE_PAYLOAD)
        current = cast(
            dict[str, object],
            payload["current"],
        )
        current.pop("temperature_2m")

        with self.assertRaises(WeatherAdapterError):
            self.adapter.adapt(payload)

    def test_adapt_invalid_json(self) -> None:
        """test adapting malformed JSON."""
        with self.assertRaises(WeatherAdapterError):
            self.adapter.adapt("{not json}")

    def test_adapt_json_array(self) -> None:
        """test adapting JSON that is not an object."""
        with self.assertRaises(WeatherAdapterError):
            self.adapter.adapt("[1, 2, 3]")

    def test_adapt_invalid_numeric_value(self) -> None:
        """test rejection of a nonnumeric weather value."""
        payload = copy.deepcopy(SAMPLE_PAYLOAD)
        current = cast(
            dict[str, object],
            payload["current"],
        )
        current["temperature_2m"] = "warm"

        with self.assertRaises(WeatherAdapterError):
            self.adapter.adapt(payload)

    @given(
        latitude=st.floats(
            min_value=-90,
            max_value=90,
            allow_nan=False,
            allow_infinity=False,
        ),
        longitude=st.floats(
            min_value=-180,
            max_value=180,
            allow_nan=False,
            allow_infinity=False,
        ),
        temperature=st.floats(
            min_value=-100,
            max_value=150,
            allow_nan=False,
            allow_infinity=False,
        ),
    )
    def test_hypothesis_adapter_preserves_values(
        self,
        latitude: float,
        longitude: float,
        temperature: float,
    ) -> None:
        """test adapter values using generated weather data."""
        payload: dict[str, object] = {
            "latitude": latitude,
            "longitude": longitude,
            "current": {
                "temperature_2m": temperature,
                "relative_humidity_2m": 50,
                "wind_speed_10m": 5.0,
                "precipitation": 0.0,
                "weather_code": 0,
            },
        }

        weather = self.adapter.adapt(payload)

        self.assertAlmostEqual(
            weather.latitude,
            latitude,
        )
        self.assertAlmostEqual(
            weather.longitude,
            longitude,
        )
        self.assertAlmostEqual(
            weather.temperature,
            temperature,
        )


if __name__ == "__main__":
    unittest.main()
