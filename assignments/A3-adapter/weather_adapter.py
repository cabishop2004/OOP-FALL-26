"""adapt Open-Meteo API responses into internal weather objects."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import cast, overload


REQUIRED_CURRENT_FIELDS: tuple[str, ...] = (
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "precipitation",
    "weather_code",
)


class WeatherAdapterError(ValueError):
    """represent invalid data received by the weather adapter."""


class WeatherData:
    """represent normalized current weather data."""

    def __init__(
        self,
        latitude: float,
        longitude: float,
        temperature: float,
        humidity: int,
        wind_speed: float,
        precipitation: float,
        weather_code: int,
    ) -> None:
        """initialize normalized weather data."""
        self.__latitude: float = latitude
        self.__longitude: float = longitude
        self.__temperature: float = temperature
        self.__humidity: int = humidity
        self.__wind_speed: float = wind_speed
        self.__precipitation: float = precipitation
        self.__weather_code: int = weather_code

    @property
    def latitude(self) -> float:
        """return the latitude."""
        return self.__latitude

    @property
    def longitude(self) -> float:
        """return the longitude."""
        return self.__longitude

    @property
    def temperature(self) -> float:
        """return the temperature in degrees Fahrenheit."""
        return self.__temperature

    @property
    def humidity(self) -> int:
        """return relative humidity as a percentage."""
        return self.__humidity

    @property
    def wind_speed(self) -> float:
        """return wind speed in miles per hour."""
        return self.__wind_speed

    @property
    def precipitation(self) -> float:
        """return precipitation in inches."""
        return self.__precipitation

    @property
    def weather_code(self) -> int:
        """return the WMO weather code."""
        return self.__weather_code


class WeatherAdapter:
    """translate third party Open-Meteo data into WeatherData."""

    @classmethod
    def required_current_fields(cls) -> tuple[str, ...]:
        """return the API fields required by the adapter."""
        return REQUIRED_CURRENT_FIELDS

    @staticmethod
    def is_supported(payload: Mapping[str, object]) -> bool:
        """return whether an API payload contains required weather data."""
        current: object = payload.get("current")

        return (
            "latitude" in payload
            and "longitude" in payload
            and isinstance(current, Mapping)
            and all(field in current for field in REQUIRED_CURRENT_FIELDS)
        )

    @overload
    def adapt(self, payload: Mapping[str, object]) -> WeatherData:
        """adapt a mapping payload."""

    @overload
    def adapt(self, payload: str) -> WeatherData:
        """adapt a JSON string payload."""

    def adapt(
        self,
        payload: Mapping[str, object] | str,
    ) -> WeatherData:
        """adapt Open-Meteo data into the application's internal format."""
        normalized: Mapping[str, object]

        if isinstance(payload, str):
            try:
                decoded: object = json.loads(payload)
            except json.JSONDecodeError as error:
                raise WeatherAdapterError("invalid JSON weather data") from error

            if not isinstance(decoded, Mapping):
                raise WeatherAdapterError(
                    "weather JSON must contain an object"
                )

            normalized = cast(Mapping[str, object], decoded)
        else:
            normalized = payload

        if not self.is_supported(normalized):
            raise WeatherAdapterError(
                "weather payload is missing required fields"
            )

        current = cast(
            Mapping[str, object],
            normalized["current"],
        )

        return WeatherData(
            latitude=self._number(normalized["latitude"], "latitude"),
            longitude=self._number(normalized["longitude"], "longitude"),
            temperature=self._number(
                current["temperature_2m"],
                "temperature_2m",
            ),
            humidity=int(
                self._number(
                    current["relative_humidity_2m"],
                    "relative_humidity_2m",
                )
            ),
            wind_speed=self._number(
                current["wind_speed_10m"],
                "wind_speed_10m",
            ),
            precipitation=self._number(
                current["precipitation"],
                "precipitation",
            ),
            weather_code=int(
                self._number(
                    current["weather_code"],
                    "weather_code",
                )
            ),
        )

    @staticmethod
    def _number(value: object, field: str) -> float:
        """convert an API value into a floating point number."""
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)

        raise WeatherAdapterError(
            f"{field} must contain a numeric value"
        )
