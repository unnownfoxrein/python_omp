"""Клиент для Open-Meteo Weather API.

Задача 2: реализовать асинхронные функции для получения данных о погоде
с внешнего API https://open-meteo.com/.

Open-Meteo — бесплатный API без ключа. Документация: https://open-meteo.com/en/docs
"""

import httpx  # noqa: F401

from app.models import WeatherCurrent, WeatherForecast  # noqa: F401

BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Параметры, которые мы запрашиваем у API для текущей погоды
CURRENT_PARAMS = (
    "temperature_2m,"
    "relative_humidity_2m,"
    "wind_speed_10m,"
    "wind_direction_10m,"
    "precipitation,"
    "cloud_cover,"
    "weather_code"
)

# Параметры для почасового прогноза
HOURLY_PARAMS = "temperature_2m,wind_speed_10m,precipitation_probability,cloud_cover"


class WeatherAPIError(Exception):
    """Ошибка при обращении к внешнему API погоды."""


# ---------------------------------------------------------------------------
# Задача 2.1: fetch_current_weather
# ---------------------------------------------------------------------------
#
# Отправьте GET-запрос к Open-Meteo API и верните текущую погоду.
#
# URL: https://api.open-meteo.com/v1/forecast
# Query-параметры:
#   latitude  = lat
#   longitude = lon
#   current   = CURRENT_PARAMS (строка выше)
#
# Пример ответа API (поле "current"):
# {
#     "temperature_2m": 8.5,
#     "relative_humidity_2m": 45,
#     "wind_speed_10m": 12.3,
#     "wind_direction_10m": 180,
#     "precipitation": 0.0,
#     "cloud_cover": 25,
#     "weather_code": 1
# }
#
# Нужно:
# 1. Создать httpx.AsyncClient и отправить GET-запрос
# 2. Проверить статус ответа (если не 200 — бросить WeatherAPIError)
# 3. Распарсить JSON и вернуть WeatherCurrent
#
# Подсказка: используйте async with httpx.AsyncClient() as client: ...


async def fetch_current_weather(lat: float, lon: float) -> WeatherCurrent:
    """Получить текущую погоду для заданных координат.

    Args:
        lat: широта (-90..90)
        lon: долгота (-180..180)

    Returns:
        WeatherCurrent с текущими погодными условиями

    Raises:
        WeatherAPIError: если API вернул ошибку или данные невалидны
    """
    # TODO: реализуйте функцию
    raise NotImplementedError("Задача 2.1: реализуйте fetch_current_weather")


# ---------------------------------------------------------------------------
# Задача 2.2: fetch_forecast
# ---------------------------------------------------------------------------
#
# Отправьте GET-запрос для получения почасового прогноза.
#
# Query-параметры:
#   latitude      = lat
#   longitude     = lon
#   hourly        = HOURLY_PARAMS
#   forecast_days = рассчитайте из hours (1 день = 24 часа, округлите вверх)
#
# ВАЖНО — формат ответа API (параллельные массивы):
# {
#     "hourly": {
#         "time": ["2025-03-15T00:00", "2025-03-15T01:00", "2025-03-15T02:00"],
#         "temperature_2m": [5.1, 4.8, 4.5],
#         "wind_speed_10m": [10.0, 11.2, 9.8],
#         "precipitation_probability": [0, 10, 20],
#         "cloud_cover": [25, 30, 40]
#     }
# }
#
# Нужно трансформировать в список объектов:
# [
#     WeatherForecast(timestamp=..., temperature=5.1, wind_speed=10.0, ...),
#     WeatherForecast(timestamp=..., temperature=4.8, wind_speed=11.2, ...),
#     WeatherForecast(timestamp=..., temperature=4.5, wind_speed=9.8, ...),
# ]
#
# Подсказка: zip() или enumerate() помогут трансформировать параллельные массивы.
# Не забудьте обрезать результат до `hours` элементов.


async def fetch_forecast(lat: float, lon: float, hours: int = 24) -> list[WeatherForecast]:
    """Получить почасовой прогноз погоды.

    Args:
        lat: широта
        lon: долгота
        hours: количество часов прогноза (по умолчанию 24)

    Returns:
        Список WeatherForecast длиной не более hours

    Raises:
        WeatherAPIError: если API вернул ошибку или данные невалидны
    """
    # TODO: реализуйте функцию
    raise NotImplementedError("Задача 2.2: реализуйте fetch_forecast")
