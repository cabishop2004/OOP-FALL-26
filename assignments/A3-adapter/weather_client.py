"""provide access to the Open-Meteo weather API."""

from __future__ import annotations

from typing import cast

import requests


BASE_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_TIMEOUT = 10.0
CURRENT_PARAMETERS = (
    "temperature_2m,"
    "relative_humidity_2m,"
    "wind_speed_10m,"
    "precipitation,"
    "weather_code"
)


class WeatherClientError(RuntimeError):
    """represent a failure while communicating with the weather API."""


class WeatherClient:
    """retrieve current weather data from Open-Meteo."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """initialize a weather API client."""
        if not base_url.strip():
            raise ValueError("base URL cannot be empty")

        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self.__base_url: str = base_url
        self.__timeout: float = timeout

    @property
    def base_url(self) -> str:
        """return the API base URL."""
        return self.__base_url

    @property
    def timeout(self) -> float:
        """return the API request timeout."""
        return self.__timeout

    @staticmethod
    def coordinates_are_valid(
        latitude: float,
        longitude: float,
    ) -> bool:
        """return whether latitude and longitude are valid."""
        return (
            -90.0 <= latitude <= 90.0
            and -180.0 <= longitude <= 180.0
        )

    def fetch_current(
        self,
        latitude: float,
        longitude: float,
    ) -> dict[str, object]:
        """retrieve current weather for a geographic coordinate."""
        if not self.coordinates_are_valid(latitude, longitude):
            raise ValueError("latitude or longitude is outside valid range")

        params: dict[str, str | float] = {
            "latitude": latitude,
            "longitude": longitude,
            "current": CURRENT_PARAMETERS,
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
        }

        try:
            response = requests.get(
                self.__base_url,
                params=params,
                timeout=self.__timeout,
            )
            response.raise_for_status()
            raw_payload: object = response.json()
        except (requests.RequestException, ValueError) as error:
            raise WeatherClientError(
                "unable to retrieve weather data"
            ) from error

        if not isinstance(raw_payload, dict):
            raise WeatherClientError(
                "weather API returned an unexpected response"
            )

        return cast(dict[str, object], raw_payload)
