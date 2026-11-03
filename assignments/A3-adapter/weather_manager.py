"""coordinate the weather API client and adapter."""

from __future__ import annotations

from typing import ClassVar

from weather_adapter import WeatherAdapter, WeatherData
from weather_client import WeatherClient


class WeatherManager:
    """manage weather retrieval using the singleton pattern."""

    __instance: ClassVar[WeatherManager | None] = None

    def __new__(cls) -> WeatherManager:
        """return the single WeatherManager instance."""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self) -> None:
        """initialize singleton collaborators once."""
        if not hasattr(self, "_WeatherManager__client"):
            self.__client: WeatherClient = WeatherClient()
            self.__adapter: WeatherAdapter = WeatherAdapter()

    @classmethod
    def instance(cls) -> WeatherManager:
        """return the singleton manager."""
        return cls()

    def get_current_weather(
        self,
        latitude: float,
        longitude: float,
    ) -> WeatherData:
        """retrieve and normalize current weather information."""
        payload: dict[str, object] = self.__client.fetch_current(
            latitude,
            longitude,
        )

        return self.__adapter.adapt(payload)
