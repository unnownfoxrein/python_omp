"""Тесты для Задачи 2: клиент погодного API.

Проверяют корректность HTTP-запросов к Open-Meteo и парсинг ответов.
25 баллов.

НЕ ИЗМЕНЯЙТЕ ЭТОТ ФАЙЛ.
"""

import pytest
import respx
from httpx import Response

from app.weather import WeatherAPIError, fetch_current_weather, fetch_forecast
from tests.mock_data import (
    MOCK_CURRENT_RESPONSE_GO,
    MOCK_CURRENT_RESPONSE_NO_GO,
    MOCK_FORECAST_RESPONSE,
    MOCK_FORECAST_RESPONSE_ALL_GOOD,
)


# =================== fetch_current_weather (8 баллов) =========================


class TestFetchCurrentWeather:
    """Тесты для fetch_current_weather."""

    @respx.mock
    async def test_success(self):
        """Успешный запрос — возвращает WeatherCurrent."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_CURRENT_RESPONSE_GO)
        )

        weather = await fetch_current_weather(45.965, 63.305)

        assert weather.temperature == 8.5
        assert weather.wind_speed == 12.3
        assert weather.wind_direction == 180
        assert weather.humidity == 45
        assert weather.precipitation == 0.0
        assert weather.cloud_cover == 25
        assert weather.weather_code == 1

    @respx.mock
    async def test_bad_weather_data(self):
        """Корректный парсинг плохой погоды."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_CURRENT_RESPONSE_NO_GO)
        )

        weather = await fetch_current_weather(45.965, 63.305)

        assert weather.temperature == 2.1
        assert weather.wind_speed == 45.0
        assert weather.precipitation == 3.2
        assert weather.cloud_cover == 90

    @respx.mock
    async def test_sends_correct_params(self):
        """Проверка отправки правильных query-параметров."""
        route = respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_CURRENT_RESPONSE_GO)
        )

        await fetch_current_weather(45.965, 63.305)

        assert route.called
        request = route.calls.last.request
        assert "latitude" in str(request.url)
        assert "longitude" in str(request.url)
        assert "current" in str(request.url)

    @respx.mock
    async def test_api_error_500(self):
        """Ошибка 500 от API — должна бросить WeatherAPIError."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(500, json={"reason": "Server Error"})
        )

        with pytest.raises(WeatherAPIError):
            await fetch_current_weather(45.965, 63.305)

    @respx.mock
    async def test_api_error_malformed_json(self):
        """Невалидный JSON — должна бросить WeatherAPIError."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json={"unexpected": "format"})
        )

        with pytest.raises((WeatherAPIError, KeyError, TypeError)):
            await fetch_current_weather(45.965, 63.305)


# =================== fetch_forecast (10 баллов) ===============================


class TestFetchForecast:
    """Тесты для fetch_forecast."""

    @respx.mock
    async def test_success_default_hours(self):
        """Успешный запрос — трансформация параллельных массивов."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_FORECAST_RESPONSE)
        )

        forecasts = await fetch_forecast(45.965, 63.305, hours=6)

        assert len(forecasts) == 6
        # Первый час
        assert forecasts[0].temperature == 8.5
        assert forecasts[0].wind_speed == 12.3
        assert forecasts[0].precipitation_probability == 0
        assert forecasts[0].cloud_cover == 25
        # Последний час
        assert forecasts[5].temperature == 9.5
        assert forecasts[5].wind_speed == 14.0

    @respx.mock
    async def test_hours_limit(self):
        """Запрос с ограничением часов — обрезать результат."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_FORECAST_RESPONSE)
        )

        forecasts = await fetch_forecast(45.965, 63.305, hours=3)

        assert len(forecasts) == 3
        assert forecasts[0].temperature == 8.5
        assert forecasts[2].temperature == 10.2

    @respx.mock
    async def test_timestamp_parsing(self):
        """Проверка парсинга временных меток."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_FORECAST_RESPONSE)
        )

        forecasts = await fetch_forecast(45.965, 63.305, hours=2)

        assert forecasts[0].timestamp.hour == 12
        assert forecasts[1].timestamp.hour == 13

    @respx.mock
    async def test_all_good_forecast(self):
        """Прогноз с хорошей погодой — все элементы корректны."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_FORECAST_RESPONSE_ALL_GOOD)
        )

        forecasts = await fetch_forecast(45.965, 63.305, hours=4)

        assert len(forecasts) == 4
        for f in forecasts:
            assert f.wind_speed >= 0
            assert 0 <= f.precipitation_probability <= 100
            assert 0 <= f.cloud_cover <= 100

    @respx.mock
    async def test_api_error_500(self):
        """Ошибка 500 — бросить WeatherAPIError."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(500, json={"reason": "Error"})
        )

        with pytest.raises(WeatherAPIError):
            await fetch_forecast(45.965, 63.305)

    @respx.mock
    async def test_sends_hourly_param(self):
        """Проверка отправки параметра hourly."""
        route = respx.get("https://api.open-meteo.com/v1/forecast").mock(
            return_value=Response(200, json=MOCK_FORECAST_RESPONSE)
        )

        await fetch_forecast(45.965, 63.305, hours=6)

        assert route.called
        request = route.calls.last.request
        assert "hourly" in str(request.url)


# =================== Обработка ошибок (5 баллов) ==============================


class TestWeatherErrorHandling:
    """Тесты обработки ошибок."""

    @respx.mock
    async def test_current_connection_error(self):
        """Ошибка соединения при запросе текущей погоды."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            side_effect=ConnectionError("Connection refused")
        )

        with pytest.raises((WeatherAPIError, ConnectionError)):
            await fetch_current_weather(45.965, 63.305)

    @respx.mock
    async def test_forecast_connection_error(self):
        """Ошибка соединения при запросе прогноза."""
        respx.get("https://api.open-meteo.com/v1/forecast").mock(
            side_effect=ConnectionError("Connection refused")
        )

        with pytest.raises((WeatherAPIError, ConnectionError)):
            await fetch_forecast(45.965, 63.305)
